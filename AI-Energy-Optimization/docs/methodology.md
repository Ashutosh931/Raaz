# Methodology

## 1. Overview
The methodology of this project follows a structured engineering workflow combining Data Science, Machine Learning, and Web Software Engineering principles.

```
+---------------------+     +--------------------+     +---------------------+
| 1. Data Engineering | --> | 2. Model Training  | --> | 3. Model Evaluation |
| - Generation/Upload |     | - Feature Matrix   |     | - Metrics (MAE, R2) |
| - Preprocessing     |     | - Random Forest    |     | - Explainability    |
+---------------------+     +--------------------+     +---------------------+
                                                                  |
+---------------------+     +--------------------+                v
| 5. User Interface   | <-- | 4. Full-Stack App  | <--------------+
| - Bootstrap 5 UI    |     | - Flask Controller |
| - Chart.js Visuals  |     | - SQLite ORM Layer |
+---------------------+     +--------------------+
```

## 2. Phase Breakdown

### Phase 1: Data Engineering & Feature Synthesis
1. **Time-Series Construction:** Continuous 180-day hourly timeline (4,320 records) synthesized with realistic astronomical and sociological behaviors.
2. **Feature Decomposition:** Datetime decomposed into `hour` (0–23), `day` (1–31), `month` (1–12), `day_of_week` (0–6), and binary `is_weekend`.
3. **Physical Load Modeling:** Baseline standby load, occupancy scaling, non-linear cooling/heating thermal curves, and categorical appliance levels (Low, Medium, High).
4. **Lag & Rolling Features:** Autoregressive features `previous_consumption` and `rolling_3h_avg` computed to capture momentum in consumption.

### Phase 2: Data Preprocessing & Cleaning
1. **Handling Missing Values:** Numerical columns imputed using median values or forward-fill.
2. **Categorical Encoding:** Categorical appliance intensity strings mapped deterministically to numerical integers (Low: 1, Medium: 2, High: 3).
3. **Outlier Filtering & Bounds:** Clipping extreme anomalies to physically valid residential limits (e.g. Temperature between 0°C and 55°C, Humidity between 10% and 100%, Min kWh floor of 0.35 kWh).

### Phase 3: Machine Learning Model Development
1. **Train/Test Splitting:** 80% training set (3,456 records) and 20% holdout test set (864 records) using a fixed random seed (`random_state=42`) for reproducibility.
2. **Model Selection:**
   - **Random Forest Regressor:** 100 decision trees, maximum depth of 14, minimum samples split of 4.
   - **Linear Regression:** Standard least-squares linear baseline.
3. **Serialization:** Trained model, feature columns, evaluation metrics, and feature importances serialized into `models/energy_model.pkl` via `joblib`.

### Phase 4: Web Application Integration
1. **Controller Routes:** Flask blueprints organized modularly for authentication, dashboard, prediction, analytics, optimization, upload, cost calculation, and settings.
2. **Database Integration:** SQLite with SQLAlchemy ORM defining User, Prediction, EnergyRecord, and Alert models.
3. **Security:** Werkzeug password hashing (PBKDF2/SHA256), session auth guards, and safe input parsing.

### Phase 5: Optimization & Recommendation Engine
1. **Dynamic Rule Processing:** Context-sensitive rule engine evaluating time of day, weather, occupancy, and predicted load to output prioritized conservation actions.
2. **Simulation Algorithm:** Interactive mathematical model calculating energy and financial savings across cooling, lighting, appliance loads, and standby power.
