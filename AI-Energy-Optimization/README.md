# AI-Based Smart Energy Consumption Prediction and Optimization System

A comprehensive, production-ready, final-year college project demonstrating real-time Machine Learning prediction, energy analytics, domestic tiered cost estimation, and dynamic energy conservation optimization.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

---

## 1. Abstract
Rapid urban growth and increased reliance on high-draw appliances have caused household electricity expenses to escalate significantly. Traditional billing only offers delayed, monthly feedback after excessive costs have accumulated. This project delivers an end-to-end intelligent platform that predicts electricity demand using an explainable **Random Forest Regressor** (\(R^2 \approx 98\%\)), benchmarks it against a **Linear Regression** baseline, estimates electricity bills across tiered domestic tariffs, and provides automated, context-aware energy-saving recommendations and an interactive simulator.

---

## 2. Problem Statement
- **Lack of Predictive Foresight:** Homeowners cannot foresee how weather or appliance habits impact daily and monthly electricity consumption.
- **Peak Grid Stress:** Unmanaged coincident usage between 18:00 and 22:00 strains the electrical grid and escalates billing tariffs.
- **Standby Phantom Loads:** Electronics in standby draw 8–10% of household power unnoticed.
- **Non-Actionable Advice:** Generic energy-saving tips lack financial projections and context-awareness.

---

## 3. Key Objectives
- Synthesize realistic residential time-series electricity records (>4,300 hourly rows) reflecting meteorological and occupant dynamics.
- Train an explainable **Random Forest Regressor** to predict energy consumption in kilowatt-hours (kWh).
- Compute evaluation metrics: **MAE**, **MSE**, **RMSE**, and **\(R^2\) Score**.
- Deliver an interactive **Energy Saving Simulator** that computes real-time monetary and kWh savings.
- Provide a responsive, energy-themed web interface with light and dark theme modes.

---

## 4. Key Features

| Feature | Description |
|---|---|
| **Executive Dashboard** | Real-time KPI cards (Today's kWh, Monthly Total, Predicted Next-Day/Month, Potential Savings, Peak Hours). |
| **Interactive AI Prediction** | Input temperature, humidity, occupant count, appliance intensity, and previous kWh to obtain instant predictions and tailored saving advice. |
| **ML Performance & Explainability** | Benchmark comparison table (Random Forest vs Linear Regression), feature importance weights, and actual vs predicted holdout curves. |
| **Visual Analytics** | 6 interactive Chart.js charts: Timeline trend, Monday–Sunday weekly bar, monthly aggregate, 24h peak profile, appliance doughnut, and temperature vs energy scatter plot. |
| **Energy Saving Simulator** | Live slider-driven simulator to calculate projected monthly and yearly money saved through AC, lighting, appliance, and peak shifting adjustments. |
| **Dataset CSV Upload** | Upload custom meter datasets; system handles data validation, missing value imputation, preview generation, and database ingestion. |
| **Electricity Cost Calculator** | Flat rate and progressive domestic utility tiered slab billing calculator (Tier 1 Lifeline, Tier 2 Standard, Tier 3 Surcharge). |
| **Consumption History** | Paginated audit trail of records and predictions with search, delete, and streaming CSV export. |
| **User Authentication & Settings** | Secure registration, login session guards, Werkzeug password hashing, and user preference customization. |
| **Theme Toggle** | Seamless light/dark mode transition with persistent preference. |

---

## 5. Technology Stack

### Backend
- **Python 3.11+**
- **Flask 3.1** (WSGI Web Framework & Modular Blueprints)
- **SQLite** (Embedded Serverless Relational Database)
- **SQLAlchemy & Flask-SQLAlchemy** (Object-Relational Mapping)
- **Werkzeug** (Security & Password Hashing)

### Machine Learning & Data Processing
- **Scikit-Learn** (Random Forest Regressor & Linear Regression)
- **Pandas** (Data wrangling, cleaning & feature extraction)
- **NumPy** (Vectorized numerical computations)
- **Joblib** (Model serialization & artifact caching)

### Frontend
- **HTML5 & CSS3** (Custom energy-themed design system)
- **JavaScript (ES6+)**
- **Bootstrap 5.3** (Responsive grid & UI components)
- **Chart.js 4.4** (Client-side interactive visualizations)
- **Bootstrap Icons**

---

## 6. System Architecture

```text
User Input / CSV Upload
         |
         v
[ Bootstrap 5 / Chart.js Web Interface ]
         |
         | HTTP POST (JSON / Form Data)
         v
[ Flask Controller & Route Blueprints ]
         |
         +---> [ Data Preprocessing & Lag Feature Engineering ]
         |                       |
         |                       v
         +---> [ Random Forest Regressor (models/energy_model.pkl) ]
         |                       |
         |                       v
         +---> [ SQLite Database (database/energy.db) ]
         |
         v
[ Live Predictions, Cost Breakdown & Optimization Advice ]
```

---

## 7. Machine Learning Pipeline

1. **Feature Set (10 Features):**
   - `hour` (0–23)
   - `day_of_week` (0–6)
   - `is_weekend` (0/1)
   - `month` (1–12)
   - `temperature` (°C)
   - `humidity` (%)
   - `number_of_people` (Occupants)
   - `appliance_usage_encoded` (1=Low, 2=Medium, 3=High)
   - `previous_consumption` (Lag 1h)
   - `rolling_3h_avg` (3h moving average)
2. **Model Performance Summary:**
   - **Random Forest Regressor:** \(R^2 = 98.02\%\), \(\text{MAE} = 0.2266\text{ kWh}\), \(\text{RMSE} = 0.3198\text{ kWh}\)
   - **Linear Regression Baseline:** \(R^2 = 83.01\%\), \(\text{MAE} = 0.7069\text{ kWh}\), \(\text{RMSE} = 0.9359\text{ kWh}\)
3. **Feature Importance Explainability:**
   - `previous_consumption`: 57.58%
   - `appliance_usage_encoded`: 18.45%
   - `hour`: 15.06%
   - `temperature`: 4.26%
   - `month`: 1.33%

---

## 8. Installation & Setup

### Prerequisites
- Python 3.11 or higher installed on your system.

### Step 1: Clone or Navigate to Project Directory
```bash
cd AI-Energy-Optimization
```

### Step 2: Create a Virtual Environment
**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 9. Running the Application

Execute the following 3 commands in order:

### 1. Generate the Synthetic Dataset (4,320 Records)
```bash
python generate_dataset.py
```

### 2. Train and Evaluate the Machine Learning Model
```bash
python train_model.py
```

### 3. Launch the Flask Web Server
```bash
python app.py
```

### Step 4: Open in Web Browser
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 10. Running Automated Tests

Run the complete Pytest validation suite:
```bash
pytest tests/test_app.py -v
```

---

## 11. Project Directory Layout

```text
AI-Energy-Optimization/
│
├── app.py                      # Flask Application Entrypoint & Factory
├── config.py                   # Central Application Configuration
├── requirements.txt            # Python Dependencies
├── README.md                   # Project Documentation
├── generate_dataset.py         # Realistic Synthetic Dataset Generator
├── train_model.py              # ML Model Training & Benchmarking Script
├── predict.py                  # Standalone CLI Prediction Demo
│
├── data/
│   ├── energy_consumption.csv  # Generated 180-Day Hourly Dataset (4,320 rows)
│   └── uploads/                # User-Uploaded CSV Datasets
│
├── models/
│   ├── __init__.py             # Database models package init
│   ├── database.py             # SQLAlchemy Models (User, Prediction, EnergyRecord, Alert, UserSetting)
│   └── energy_model.pkl        # Serialized ML Model Artifact
│
├── database/
│   └── energy.db               # SQLite Database File
│
├── ml/
│   ├── __init__.py
│   ├── preprocessing.py        # Feature Engineering, Cleansing & Imputation
│   ├── train.py                # Model Training & Evaluation Logic
│   ├── prediction.py           # ML Inference Pipeline & Singleton Wrapper
│   └── optimization.py         # Dynamic Recommendation Engine & Simulator Math
│
├── routes/
│   ├── __init__.py             # Blueprints Registry
│   ├── auth.py                 # User Registration, Login & Logout
│   ├── dashboard.py            # Dashboard Controller & Chart.js API
│   ├── prediction.py           # Prediction Page & API
│   ├── analytics.py            # Visual Analytics & Scatter Feeds
│   ├── optimization.py         # Optimization & Simulator API
│   ├── upload.py               # Dataset Upload & Cleansing
│   ├── model_performance.py    # Model Benchmark & Explainability
│   ├── cost_calculator.py      # Electricity Billing & Tier Slabs
│   ├── history.py              # Consumption History & CSV Export
│   ├── settings.py             # User Preferences & Profile
│   └── about.py                # Academic Project Summary
│
├── templates/
│   ├── base.html               # Master Layout with Responsive Sidebar & Topbar
│   ├── login.html              # Sign In Page
│   ├── register.html           # User Registration Page
│   ├── dashboard.html          # Main Dashboard
│   ├── prediction.html         # Predict Energy Consumption Page
│   ├── analytics.html          # Visual Analytics Dashboard
│   ├── optimization.html       # Energy Optimization & Live Simulator
│   ├── upload.html             # CSV Upload & Preview Page
│   ├── model_performance.html  # ML Metrics & Explainability Page
│   ├── cost_calculator.html    # Electricity Tariff & Tier Calculator
│   ├── history.html            # Consumption Audit Logs & Export
│   ├── settings.html           # Profile & Preferences Settings
│   └── about.html              # Project Specifications & Viva Cheat Sheet
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom Energy-Themed Design System (Light/Dark)
│   └── js/
│       ├── main.js             # Theme Toggler, Mobile Navigation & Alerts
│       ├── dashboard.js        # Dashboard Chart.js Widgets
│       ├── analytics.js        # Analytics Charts & Scatter Plots
│       └── simulator.js        # Live Energy Saving Simulator Calculations
│
├── tests/
│   ├── __init__.py
│   └── test_app.py             # Automated Pytest Suite
│
└── docs/
    ├── abstract.md             # Project Abstract
    ├── problem_statement.md    # Problem Statement & Challenges
    ├── objectives.md           # Project Goals
    ├── methodology.md          # Data Science & Engineering Methodology
    ├── system_requirements.md  # Hardware & Software Specifications
    ├── system_architecture.md  # Architectural Diagrams & Data Flow
    ├── modules.md              # Detailed Breakdown of All 12 Modules
    ├── database_design.md      # Relational ER Schema & Table Specs
    ├── machine_learning.md     # ML Formulas, Metrics & Feature Importance
    ├── testing.md              # Test Plan & Automated Test Cases
    ├── future_scope.md         # Future Enhancements & IoT Integration
    ├── conclusion.md           # Academic Summary & Conclusions
    └── viva_questions.md       # 32 Comprehensive Viva Q&As
```

---

## 12. Academic Viva Preparation
For college project defense, refer to the documentation in `docs/`:
- `docs/viva_questions.md`: Over 32 detailed questions and answers covering ML algorithms, evaluation metrics (MAE, RMSE, \(R^2\)), backend design, and project defense strategies.
- `docs/machine_learning.md`: Full mathematical equations and feature importance rankings.

---

## 13. License
This project is open-source and available under the [MIT License](LICENSE).
