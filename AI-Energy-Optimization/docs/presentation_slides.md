# Presentation Slides & Viva Speaker Notes

This document provides the slide-by-slide content and speaker presentation script corresponding to [`presentation.pptx`](file:///c:/Users/Ashutosh%20Yadav/OneDrive/Desktop/AI-Energy-Optimization/presentation.pptx).

---

## Slide 1: Title Slide
- **Title:** AI-Based Smart Energy Consumption Prediction and Optimization System
- **Subtitle:** Final Year Capstone Project Presentation & Viva Defense
- **Tech Stack:** Python 3.11, Flask, Random Forest Regressor, Scikit-Learn, SQLite, Bootstrap 5, Chart.js
- **Speaker Note:** *"Good morning respected evaluators. Today I am presenting our final-year project: 'AI-Based Smart Energy Consumption Prediction and Optimization System', an end-to-end intelligent platform that predicts electricity demand using Machine Learning, calculates electricity costs across domestic tariff tiers, and provides personalized energy conservation recommendations."*

---

## Slide 2: Introduction & Background Motivation
- **The Energy Crisis & Billing Gap:**
  - Surging residential electricity usage from heavy appliances (ACs, geysers, EV charging).
  - Traditional utility bills provide delayed feedback after high costs have already accumulated.
  - Consumers lack visibility into which appliances or hours cause spikes.
- **Why Machine Learning:**
  - Energy usage involves complex weather and human schedule interactions that static rules cannot model.
  - ML provides predictive foresight: projecting consumption so users can act proactively.
  - Helps households save 15% to 30% while reducing grid peak demand.

---

## Slide 3: Problem Statement
- **Lack of Predictive Foresight:** No tool to estimate energy demand before running high-draw appliances.
- **Peak Grid Demand Strain:** Heavy coincident usage during 18:00–22:00 overburdens the electrical grid and inflates utility tariffs.
- **Vampire / Standby Losses:** Standby power draws 8%–10% unnoticed.
- **Generic Inactionable Tips:** Standard tips lack mathematical context and financial projections.

---

## Slide 4: Project Objectives & Scope
- **Machine Learning Goals:**
  - Synthesize realistic 4,320-record residential energy dataset.
  - Train an explainable Random Forest Regressor (\(R^2 > 95\%\)).
  - Benchmark against a Linear Regression baseline.
  - Evaluate MAE, MSE, RMSE, and \(R^2\) score metrics.
  - Extract feature importance rankings for model explainability.
- **Software Engineering Goals:**
  - Build a 3-tier MVC full-stack web application with Flask and SQLAlchemy.
  - Implement secure authentication and password hashing (PBKDF2/SHA256).
  - Build an interactive Energy Saving Simulator.
  - Deliver responsive visualizations using Bootstrap 5 and Chart.js.

---

## Slide 5: System Architecture & Workflow
- **Presentation Layer:** HTML5, CSS3 with Light/Dark theme toggle, Bootstrap 5, 6 Chart.js widgets, reactive sliders.
- **Application Controller Layer:** Flask 3.1 WSGI application with modular route blueprints, lag feature engineering, dynamic optimization engine, and tiered billing calculators.
- **ML & Storage Layer:** Serialized Random Forest model (`models/energy_model.pkl`), SQLite database (`database/energy.db`), SQLAlchemy ORM models.

---

## Slide 6: Dataset & Feature Engineering
- **Synthesized Dataset (4,320 Records):**
  - 180 continuous days with hourly resolution.
  - Physics-grounded cooling demand (AC kicks in above 26°C).
  - Diurnal cycles: morning surge (07:00–09:00), workday lull, evening peak (18:00–22:00).
- **10 Predictive Features:**
  - `hour`, `day`, `month`, `day_of_week`, `is_weekend`
  - `temperature`, `humidity`
  - `number_of_people`, `appliance_usage_encoded`
  - `previous_consumption` (Lag 1h), `rolling_3h_avg`

---

## Slide 7: Algorithm Selection (Why Random Forest?)
- **Why Random Forest:**
  - Ensemble of 100 decision trees via bootstrap aggregation (bagging) to minimize variance.
  - Handles non-linear thermal thresholds (e.g. AC power scaling above 28°C) without manual polynomial features.
  - Constrained with `max_depth=14` and `min_samples_split=4` to prevent overfitting.
  - Provides transparent Gini feature importance rankings.
- **Why Not Linear Regression or Deep Learning:**
  - Linear Regression fails on non-linear threshold curves.
  - Deep Learning / LSTMs require large datasets, GPUs, and act as "black-box" models.
  - Random Forest trains in seconds on CPUs and is explainable.

---

## Slide 8: Model Performance & Benchmark Results
- **Random Forest Regressor (Primary Model):**
  - \(R^2\) Score: **0.9802 (98.02%)**
  - Mean Absolute Error (MAE): **0.2266 kWh**
  - Root Mean Squared Error (RMSE): **0.3198 kWh**
- **Linear Regression (Baseline Benchmark):**
  - \(R^2\) Score: **0.8301 (83.01%)**
  - Mean Absolute Error (MAE): **0.7069 kWh**
  - Root Mean Squared Error (RMSE): **0.9359 kWh**
- **Performance Delta:** Random Forest improves \(R^2\) by +15.01% and reduces prediction error by 67.9%.

---

## Slide 9: Model Explainability (Feature Importance)
- **Rankings:**
  1. `previous_consumption`: **57.58%** (Lag energy momentum)
  2. `appliance_usage_encoded`: **18.45%** (Active load intensity)
  3. `hour`: **15.06%** (Diurnal curve)
  4. `temperature`: **4.26%** (Thermal cooling demand)
  5. `month`: **1.33%** (Seasonality)
- **Viva Note:** Explains that electricity consumption is highly autoregressive, with evening lifestyle patterns and appliance modes contributing over 33% of predictive power.

---

## Slide 10: Interactive Prediction & Cost Calculator
- **Prediction Page:** User inputs environmental and household parameters to get instant predicted kWh, estimated hourly/daily/monthly costs, and categorization (Low, Normal, High).
- **Progressive Domestic Tier Slabs:**
  - Tier 1 (0–100 kWh): 60% base rate (Lifeline)
  - Tier 2 (101–300 kWh): 100% base rate (Standard)
  - Tier 3 (>300 kWh): 135% base rate (Heavy surcharge)

---

## Slide 11: Dynamic Optimization & Recommendations
- **Context-Aware Rules:**
  - Peak hour shifting (18:00–22:00) saves ~₹432/mo.
  - AC thermostat 24°C–26°C saves ~6% per °C.
  - AC "Dry Mode" during high humidity saves up to 25% compressor power.
  - Standby power elimination saves ~₹160/mo.
- **Quantified Output:** Displays projected monthly money saved (₹) and energy reduced (kWh).

---

## Slide 12: Interactive Energy Saving Simulator
- **Sliders & Toggles:**
  - Reduce AC / Cooling Usage (0% to 50%)
  - Optimize Lighting (0% to 50%)
  - Reduce Major Appliances (0% to 50%)
  - Shift Peak Hours (0% to 50%)
  - Eliminate Standby Vampire Draw toggle
- **Live Output:** Monthly/Yearly money saved, projected bill, overall reduction percentage progress bar.

---

## Slide 13: Dataset Upload & Visual Analytics
- **Dataset Upload:** Validates CSV, standardizes headers, imputes missing values, and bulk ingests into SQLite.
- **6 Chart.js Visualizations:** Timeline trend line chart, weekday comparison bar chart, monthly aggregate chart, 24h peak usage profile, appliance doughnut chart, temperature vs energy scatter plot.

---

## Slide 14: Testing, Security & Verification
- **Automated Pytest Suite (7/7 Passed):** Tests data preprocessing, prediction math, tiered billing, simulator calculations, user auth, and CSV validation.
- **Security:** Password hashing with PBKDF2/SHA256, session authentication guards, physical input boundary checks, and SQLAlchemy parameterization.

---

## Slide 15: Conclusion & Future Scope
- **Conclusion:** Production-ready, explainable AI system achieving 98.02% accuracy and enabling 15%–30% bill reductions completely offline.
- **Future Scope:** IoT CT current sensor telemetry, automated smart plug actuation, rooftop solar PV net-metering, and mobile PWA alerts.
