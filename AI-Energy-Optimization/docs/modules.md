# System Modules

The application is structured into 12 distinct, modular subsystems:

## 1. Authentication & Session Module (`routes/auth.py`)
- Manages user registration, login, session persistence, and logout.
- Utilizes PBKDF2/SHA-256 password hashing with salt.
- Auto-seeds a newly registered user account with 7 days of realistic baseline records to ensure the dashboard renders rich metrics immediately.

## 2. Executive Dashboard Module (`routes/dashboard.py`)
- Calculates real-time KPI metrics: Today's consumption, monthly total, next-day prediction, next-month prediction, estimated bill, potential savings, and extreme consumption days.
- Serves aggregated JSON chart feeds for daily trend, peak usage hours, appliance share, and actual vs predicted comparisons.

## 3. Machine Learning Prediction Module (`routes/prediction.py`, `ml/prediction.py`)
- Implements the real-time inference interface for the Random Forest model.
- Validates user input bounds (e.g. valid temperatures, non-negative previous kWh).
- Performs instant categorization (Low: < 3.5 kWh, Normal: 3.5–7.5 kWh, High: > 7.5 kWh) and triggers automated warnings.

## 4. Visual Analytics Module (`routes/analytics.py`)
- Delivers 6 interactive visualizations:
  1. Timeline trend line chart
  2. Weekday bar chart (Monday through Sunday)
  3. Monthly aggregated usage
  4. 24-hour diurnal peak load profile
  5. Appliance category doughnut breakdown
  6. Temperature vs energy consumption scatter plot.

## 5. Energy Optimization & Simulator Module (`routes/optimization.py`, `ml/optimization.py`)
- **Dynamic Recommendation Engine:** Evaluates ambient weather, time of day, occupancy, and appliance load to generate prioritized, context-aware conservation advice.
- **Energy Saving Simulator:** An interactive slider-driven tool that calculates projected monthly and yearly money saved and energy reduced.

## 6. Dataset Ingestion & Cleansing Module (`routes/upload.py`, `ml/preprocessing.py`)
- Processes user-uploaded CSV files up to 16MB.
- Standardizes headers, calculates missing lag features, and imputes null values using median statistics.
- Provides a downloadable sample CSV template (`/download-sample-csv`).

## 7. Model Performance & Explainability Module (`routes/model_performance.py`, `ml/train.py`)
- Displays side-by-side evaluation metrics comparing Random Forest Regressor and Linear Regression baseline (MAE, MSE, RMSE, R²).
- Features a Feature Importance horizontal bar chart to explain model decisions.
- Visualizes actual vs predicted curves across 30 holdout test samples.

## 8. Electricity Cost Calculator Module (`routes/cost_calculator.py`)
- Calculates daily, weekly, monthly, and yearly costs.
- Implements standard progressive domestic utility tiered pricing (Tier 1 Lifeline, Tier 2 Standard, Tier 3 Heavy surcharge).
- Supports customizable currencies (₹, $, €, £).

## 9. History & Audit Log Module (`routes/history.py`)
- Displays paginated records of historical energy consumption and ML prediction logs.
- Enables filtering, single-record deletion, and streaming CSV export.

## 10. Settings & Preferences Module (`routes/settings.py`)
- Allows users to update profile details, billing currency, default tariff rate per kWh, and password.
- Provides alert history clearing tools.

## 11. About & Viva Cheat Sheet Module (`routes/about.py`)
- Presents the academic abstract, objectives, architecture flow, and viva defense checklist.

## 12. Automated Testing Module (`tests/test_app.py`)
- Automated Pytest suite verifying auth routes, ML prediction math, preprocessing, and cost calculations.
