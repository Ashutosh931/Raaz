# System Architecture

## 1. Architectural Overview
The **AI-Based Smart Energy Consumption Prediction and Optimization System** adopts a 3-tier Model-View-Controller (MVC) architecture ensuring separation of concerns between user presentation, business and machine learning logic, and persistent storage.

```
+-----------------------------------------------------------------------+
|                           PRESENTATION LAYER                          |
|  - HTML5 & CSS3 Responsive Layouts                                    |
|  - Bootstrap 5 & Custom Energy Design System                          |
|  - Chart.js Dynamic Visualizations (Line, Bar, Doughnut, Scatter)     |
|  - Theme Controller (Light / Dark Mode via CSS Tokens)                |
+-----------------------------------------------------------------------+
                                   |
                                   | HTTP / AJAX Requests (JSON / Form Data)
                                   v
+-----------------------------------------------------------------------+
|                          APPLICATION CONTROLLER                       |
|                          (Flask Python 3.11+)                         |
|  - Blueprints: Auth, Dashboard, Predict, Analytics, Optimization,    |
|    Upload, Cost Calculator, Model Performance, History, Settings      |
|  - Session Manager & Authentication Guard (Werkzeug Security)         |
|  - Jinja2 Template Engine & Context Processors                        |
+-----------------------------------------------------------------------+
           |                                               |
           | ML Feature Extraction                         | ORM Queries (SQL)
           v                                               v
+------------------------------------+   +------------------------------+
|       MACHINE LEARNING LAYER       |   |       DATA STORAGE LAYER     |
| - Preprocessing & Lag Engineering  |   | - SQLite Database (energy.db)|
| - Random Forest Regressor (100 T)  |   | - User Table                 |
| - Model Artifacts (energy_model.pkl|   | - EnergyRecord Table         |
| - Explainability & Feature Weights |   | - Prediction Table           |
| - Rule-Based Recommendation Engine |   | - Alert & UserSetting Tables |
| - Energy Saving Simulator Engine   |   +------------------------------+
+------------------------------------+
```

## 2. Component Flow & Interactions

### A. Real-Time Energy Prediction Flow
1. The user navigates to the **Predict Consumption** page and fills in environmental parameters (Date, Time, Temperature, Humidity, Occupants, Appliance Usage, Previous kWh).
2. The browser submits a POST request to `/predict`.
3. The Flask controller sanitizes input values and passes them to `EnergyPredictor`.
4. `EnergyPredictor` constructs the normalized 10-feature vector `[hour, day_of_week, is_weekend, month, temperature, humidity, number_of_people, appliance_usage_encoded, previous_consumption, rolling_3h_avg]`.
5. The preloaded Random Forest model computes the predicted consumption in kWh.
6. The controller calculates the estimated cost (\(\text{kWh} \times \text{Tariff}\)), categorizes the usage (Low, Normal, High), generates dynamic contextual tips, saves the record to the database, and renders the result view.

### B. Dataset Upload & Ingestion Flow
1. The user selects a CSV file on the **Upload Dataset** page.
2. Flask validates the file extension and MIME type and saves the file to `data/uploads/`.
3. `ml/preprocessing.py` validates the schema, standardizes column headers, computes missing lag values, and imputes missing weather/occupant values.
4. Cleaned records are bulk-saved into the SQLite `EnergyRecord` table, updating user dashboard metrics and analytics charts immediately.
