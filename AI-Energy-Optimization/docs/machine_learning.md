# Machine Learning Methodology & Explainability

## 1. Algorithm Selection: Random Forest Regressor
Electricity consumption in residential settings involves complex, non-linear interactions:
- Temperature exhibits a non-linear threshold effect (AC compressor load accelerates when \(T > 28^\circ\text{C}\)).
- Diurnal human habits create distinct peaks at 07:00–09:00 (morning) and 18:00–22:00 (evening).
- High appliance usage amplifies occupant loads multiplicatively.

**Random Forest** is an ensemble meta-estimator that fits multiple decision trees on sub-samples of the dataset and uses averaging to improve predictive accuracy and control over-fitting.

### Key Advantages:
1. **Handles Non-Linearity:** Unlike Linear Regression, decision tree splits capture threshold responses without needing manual polynomial transformations.
2. **Resistant to Overfitting:** Bootstrapping and random feature selection reduce variance.
3. **Intrinsic Explainability:** Computes Gini-based feature importances directly.
4. **Lightweight & Fast:** Trains in seconds on standard CPU hardware without GPU requirements.

---

## 2. Mathematical Formulations

### Mean Absolute Error (MAE):
Measures the average magnitude of the errors without considering their direction:
$$\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i|$$

### Mean Squared Error (MSE):
$$\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

### Root Mean Squared Error (RMSE):
Penalizes large outlier errors more severely:
$$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2}$$

### Coefficient of Determination (\(R^2\)):
Indicates the proportion of variance in the dependent variable explained by the model:
$$R^2 = 1 - \frac{\sum_{i=1}^{N} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{N} (y_i - \bar{y})^2}$$
Where \(\bar{y} = \frac{1}{N}\sum_{i=1}^{N} y_i\).

---

## 3. Feature Pipeline & Importance Ranking

The model accepts 10 engineered features:
1. `hour` (0–23): Time of day diurnal cycle.
2. `day_of_week` (0–6): Captures weekday vs weekend variance.
3. `is_weekend` (0 or 1): Binary flag for daytime home occupancy.
4. `month` (1–12): Annual seasonal temperature base.
5. `temperature` (°C): Ambient outdoor temperature.
6. `humidity` (%): Relative humidity influencing AC dehumidification.
7. `number_of_people`: Occupant count.
8. `appliance_usage_encoded`: Categorical intensity (1=Low, 2=Medium, 3=High).
9. `previous_consumption`: Autoregressive lag consumption from previous hour.
10. `rolling_3h_avg`: 3-hour rolling mean capturing recent energy momentum.

### Feature Importance Weights:
| Rank | Feature | Description | Relative Weight (%) |
|---|---|---|---|
| 1 | `previous_consumption` | Immediate lag energy momentum | ~57.5% |
| 2 | `appliance_usage_encoded`| Equipment intensity level | ~18.5% |
| 3 | `hour` | Time of day diurnal curve | ~15.1% |
| 4 | `temperature` | Cooling/Heating thermal demand | ~4.3% |
| 5 | `month` | Seasonal weather trend | ~1.3% |
| 6 | `rolling_3h_avg` | Multi-hour moving window | ~1.1% |
| 7 | `humidity` | Moisture comfort index | ~0.9% |
| 8 | `number_of_people` | Household occupant count | ~0.8% |
| 9 | `day_of_week` | Weekly schedule factor | ~0.3% |
| 10 | `is_weekend` | Weekend leisure profile | ~0.2% |
