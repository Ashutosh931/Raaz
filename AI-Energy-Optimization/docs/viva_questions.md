# Comprehensive Viva Questions and Answers (30+ Questions)

This document contains 32 frequently asked viva questions and clear, college-level answers tailored for presenting the **“AI-Based Smart Energy Consumption Prediction and Optimization System”**.

---

### Q1: What is the main objective of your project?
**Answer:** The primary objective is to build an intelligent web application that analyzes historical electricity consumption data, predicts future electricity demand using Machine Learning (Random Forest Regressor), calculates electricity costs across domestic tariff tiers, and provides personalized, context-aware energy-saving recommendations to reduce consumer utility bills and grid peak demand.

---

### Q2: Why did you choose this project?
**Answer:** Electricity bills are a major recurring household expense, yet consumers only receive delayed feedback via monthly bills without knowing which appliances or habits caused high costs. By leveraging Machine Learning, we can give users proactive predictive foresight, enabling them to optimize appliance scheduling and lower consumption before high bills accumulate.

---

### Q3: What is Machine Learning?
**Answer:** Machine Learning is a branch of Artificial Intelligence where algorithms learn mathematical patterns and relationships from historical data to make accurate predictions on new, unseen data without being explicitly hardcoded with fixed rules.

---

### Q4: What type of Machine Learning problem is this?
**Answer:** This is a **Supervised Regression** problem:
- **Supervised:** Because the training dataset contains both input features (weather, occupancy, hour) and labeled ground-truth targets (`energy_consumption` in kWh).
- **Regression:** Because the target variable being predicted is continuous (a numerical value in kilowatt-hours, e.g., 4.85 kWh) rather than categorical.

---

### Q5: Why did you choose Random Forest Regressor?
**Answer:** 
1. **Non-linear Relationship Handling:** Electricity consumption depends non-linearly on temperature (e.g., exponential cooling load above 28°C) and time of day. Random Forest captures complex threshold splits easily.
2. **Resistance to Overfitting:** It uses bootstrap aggregation (bagging) and random feature subset selection across 100 decision trees to reduce model variance.
3. **Explainability:** It provides intrinsic feature importance scores, making the predictions transparent.
4. **Computational Efficiency:** It trains rapidly on CPU hardware without requiring GPUs.

---

### Q6: Why compare Random Forest with Linear Regression?
**Answer:** In academic research, it is essential to establish a baseline model. Linear Regression assumes a straight-line linear relationship (\(y = \beta_0 + \beta_1 x_1 + \dots\)), which fails to model diurnal peaks and non-linear AC compressor thresholds. Comparing both proves that Random Forest achieves superior accuracy (\(R^2 = 98.0\%\) vs \(83.0\%\) for Linear Regression).

---

### Q7: What is Training Data and Testing Data?
**Answer:** 
- **Training Data (80%):** The portion of historical data (3,456 records) used by the algorithm to adjust its decision tree split parameters and learn underlying energy patterns.
- **Testing Data (20%):** A separate holdout dataset (864 records) never seen during training, used exclusively to evaluate how well the model generalizes to new data.

---

### Q8: What is Overfitting and how do you prevent it?
**Answer:** Overfitting happens when a model memorizes training noise and performs poorly on new test data. We prevent overfitting by:
1. Using Random Forest ensemble averaging.
2. Setting `max_depth=14` and `min_samples_split=4` to constrain tree complexity.
3. Evaluating performance on an independent 20% holdout test set.

---

### Q9: What is Underfitting?
**Answer:** Underfitting occurs when a model is too simplistic to capture the underlying trends in data (for instance, simple Linear Regression trying to model complex cyclical hourly loads), leading to high training error and high testing error.

---

### Q10: What is Mean Absolute Error (MAE)?
**Answer:** MAE is the average absolute difference between the actual energy consumption and the predicted energy consumption:
$$\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i|$$
Our model achieves an MAE of **~0.23 kWh**, meaning predictions deviate by only ~0.23 units on average.

---

### Q11: What is Mean Squared Error (MSE)?
**Answer:** MSE is the average of the squared differences between actual and predicted values:
$$\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$
Squaring heavily penalizes larger prediction mistakes.

---

### Q12: What is Root Mean Squared Error (RMSE)?
**Answer:** RMSE is the square root of MSE:
$$\text{RMSE} = \sqrt{\text{MSE}}$$
It is expressed in the same physical units as the target variable (kWh). Our model achieves an RMSE of **~0.32 kWh**.

---

### Q13: What is \(R^2\) Score (Coefficient of Determination)?
**Answer:** The \(R^2\) score measures the proportion of variance in the target variable that is explained by the input features relative to a simple mean baseline:
$$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$
An \(R^2\) of 1.0 (100%) represents perfect prediction. Our model achieves **\(R^2 \approx 0.9802\) (98.0%)**.

---

### Q14: What features are used for prediction?
**Answer:** The model uses 10 engineered features:
1. `hour` (0–23)
2. `day_of_week` (0–6)
3. `is_weekend` (0/1)
4. `month` (1–12)
5. `temperature` (°C)
6. `humidity` (%)
7. `number_of_people`
8. `appliance_usage_encoded` (1=Low, 2=Medium, 3=High)
9. `previous_consumption` (Lag 1h)
10. `rolling_3h_avg` (3h moving average)

---

### Q15: Which feature is the most important according to the model?
**Answer:** `previous_consumption` (lag momentum) is the most significant feature (~57.5% weight), followed by `appliance_usage_encoded` (~18.5%), `hour` (~15.1%), and `temperature` (~4.3%).

---

### Q16: Why use Flask for the backend?
**Answer:** Flask is a lightweight, modular, and performant Python WSGI web framework. It provides full flexibility to integrate Scikit-Learn models, SQLAlchemy ORM, and custom route blueprints without the unnecessary boilerplate overhead of heavier frameworks.

---

### Q17: Why use SQLite for the database?
**Answer:** SQLite is a serverless, zero-configuration, self-contained embedded database engine. It stores data locally in a single file (`database/energy.db`), ensuring that the project runs immediately on any system without setting up external database servers like MySQL or PostgreSQL.

---

### Q18: What is SQLAlchemy?
**Answer:** SQLAlchemy is an Object-Relational Mapper (ORM) for Python. It allows developers to interact with the relational database using clean Python classes and objects (`User`, `Prediction`, `EnergyRecord`) instead of writing raw SQL strings, preventing SQL injection vulnerabilities.

---

### Q19: How are passwords secured in the database?
**Answer:** Passwords are never stored in plain text. We use `werkzeug.security.generate_password_hash`, which applies PBKDF2 with SHA-256 and cryptographic salts. When logging in, `check_password_hash` verifies the hash safely.

---

### Q20: How does the system calculate electricity costs?
**Answer:** Cost calculation supports two models:
1. **Flat Tariff:** \(\text{Cost} = \text{kWh} \times \text{Tariff Rate}\) (e.g. \(10 \text{ kWh} \times \text{₹8/kWh} = \text{₹80}\)).
2. **Progressive Tiered Slabs:**
   - Tier 1 (0–100 kWh): 60% of base tariff (Lifeline slab)
   - Tier 2 (101–300 kWh): 100% of base tariff
   - Tier 3 (>300 kWh): 135% of base tariff (Heavy usage surcharge).

---

### Q21: How does the dynamic optimization engine work?
**Answer:** The recommendation engine dynamically analyzes contextual inputs:
- If current time is during peak hours (18:00–22:00), it advises shifting heavy appliances to morning or late night.
- If temperature > 28°C, it recommends setting AC thermostats to 24°C–26°C (saving 6% per °C).
- If humidity > 70%, it suggests AC "Dry Mode" (saving up to 25% compressor energy).
- It calculates tangible monthly savings in both kWh and currency (₹).

---

### Q22: What is the Energy Saving Simulator?
**Answer:** The simulator allows users to adjust interactive sliders (reduce AC by X%, reduce lighting by Y%, reduce appliances by Z%, shift peak loads) and calculates real-time projected monetary and kWh savings based on empirical residential energy component weightages.

---

### Q23: How does the CSV Upload and Data Cleansing work?
**Answer:** When a user uploads a CSV:
1. Format and size are validated (<16MB).
2. Headers are normalized to lowercase snake_case.
3. Date/time strings are decomposed into datetime features.
4. Missing numeric values are imputed using column medians or forward fills.
5. Cleaned records are ingested into SQLite and instantly reflected in dashboard analytics.

---

### Q24: What is Bootstrap 5 and Chart.js?
**Answer:**
- **Bootstrap 5:** A modern frontend CSS framework providing responsive grid layouts, cards, modals, and mobile navigation.
- **Chart.js:** An HTML5 Canvas-based JavaScript visualization library used to render interactive line, bar, doughnut, and scatter charts.

---

### Q25: Why didn't you use Deep Learning (e.g., LSTM or Neural Networks)?
**Answer:** 
1. Deep Learning requires large amounts of data (hundreds of thousands of rows) and extensive training time on GPUs.
2. LSTMs are "black-box" models that lack intuitive feature importance explainability.
3. On tabular time-series features with meteorological inputs, tree-based ensemble models (Random Forest) consistently match or outperform neural networks while remaining explainable and lightweight.

---

### Q26: What is Vampire Power / Standby Power?
**Answer:** Vampire power is the electrical power consumed by electronic devices (TVs, chargers, microwave clocks) while they are turned off or in standby mode. It accounts for roughly 8% to 10% of total residential consumption.

---

### Q27: What happens if an invalid input (e.g. negative energy or invalid date) is entered?
**Answer:** The application implements robust server-side validation. Numerical inputs are constrained within physically valid ranges (e.g. temperature -10°C to 60°C, non-negative previous kWh), and informative flash error alerts are displayed to guide the user without crashing the server.

---

### Q28: How does the model serialize and persist?
**Answer:** The trained model, feature names, baseline comparison models, and evaluation metrics are packaged into a single dictionary artifact and serialized to `models/energy_model.pkl` using the `joblib` library. When Flask starts, the `EnergyPredictor` singleton loads it into memory for instant sub-millisecond inference.

---

### Q29: What are the main limitations of this system?
**Answer:**
1. Currently relies on manual input or CSV batch upload rather than automated real-time IoT hardware telemetry.
2. Does not yet account for local solar PV generation (net-metering).
3. Trained on standard residential appliance profiles; industrial three-phase loads would require specialized training datasets.

---

### Q30: What is the future scope of this project?
**Answer:**
1. Integrating ESP32 / IoT CT current sensors for live hardware telemetry.
2. Automated smart plug actuation to cut non-essential loads during peak tariffs.
3. Solar PV irradiance forecasting and battery storage charge/discharge optimization.
4. Packaging into a mobile Progressive Web App (PWA) with push alert notifications.

---

### Q31: How do you demonstrate this project during the viva?
**Answer:** 
1. **Show Dashboard:** Explain the KPI cards (Today's kWh, Monthly cost, Savings %) and Chart.js daily/peak charts.
2. **Show Predict Page:** Enter sample values (e.g. 32°C, 4 people, High appliance) -> Click Predict -> Show predicted kWh, estimated bill, category badge, and dynamic saving tips.
3. **Show Model Performance Page:** Highlight Random Forest \(R^2 = 98.0\%\) vs Linear Regression \(83.0\%\) and explain the Feature Importance chart.
4. **Show Energy Saving Simulator:** Move the AC and Peak Shift sliders to demonstrate live recalculation of monthly savings.
5. **Show Upload Page:** Upload a sample CSV to demonstrate data cleansing, imputation, and database ingestion.

---

### Q32: What commands are needed to run the application from scratch?
**Answer:**
```bash
python generate_dataset.py
python train_model.py
python app.py
```
The application will launch and be accessible at `http://127.0.0.1:5000`.
