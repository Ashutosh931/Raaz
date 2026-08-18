"""
Energy Prediction Engine
Loads the trained Random Forest model and performs real-time single and batch inferences.
"""

import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional, List

from .preprocessing import FEATURE_COLUMNS, APPLIANCE_MAPPING, clean_dataset
from .optimization import generate_smart_recommendations

class EnergyPredictor:
    """Singleton model wrapper for efficient real-time ML inference."""
    _instance = None
    _artifact = None
    _model = None

    @classmethod
    def get_instance(cls, model_path: str = "models/energy_model.pkl"):
        if cls._instance is None:
            cls._instance = cls(model_path)
        return cls._instance

    def __init__(self, model_path: str = "models/energy_model.pkl"):
        self.model_path = model_path
        self.load_model()

    def load_model(self):
        """Loads model artifact from disk or trains a fallback if missing."""
        if not os.path.exists(self.model_path):
            # Check if dataset exists to train
            dataset_path = "data/energy_consumption.csv"
            if not os.path.exists(dataset_path):
                from generate_dataset import generate_energy_dataset
                generate_energy_dataset(output_path=dataset_path)
            from .train import train_energy_models
            self._artifact = train_energy_models(dataset_path=dataset_path, model_save_path=self.model_path)
        else:
            self._artifact = joblib.load(self.model_path)

        self._model = self._artifact.get("model")
        print("EnergyPredictor: ML Model loaded successfully.")

    def predict(
        self,
        date_str: str,
        time_str: str,
        temperature: float,
        humidity: float,
        number_of_people: int,
        appliance_usage: str,
        previous_consumption: float,
        tariff_per_kwh: float = 8.0,
        currency: str = "₹"
    ) -> Dict[str, Any]:
        """
        Executes single-point ML prediction and returns metrics, category, and saving advice.
        """
        if self._model is None:
            self.load_model()

        # Parse Date and Time
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except Exception:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
            except Exception:
                dt = datetime.now()

        hour = dt.hour
        month = dt.month
        day_of_week = dt.weekday()
        is_weekend = 1 if day_of_week in [5, 6] else 0

        # Encode appliance usage
        app_clean = str(appliance_usage).strip().lower()
        app_encoded = APPLIANCE_MAPPING.get(app_clean, 2)

        # Estimate rolling 3h average if not explicitly given
        rolling_3h_avg = round(float(previous_consumption * 0.95 + 0.1), 2)

        # Construct single-row DataFrame matching training feature columns
        feature_dict = {
            "hour": [int(hour)],
            "day_of_week": [int(day_of_week)],
            "is_weekend": [int(is_weekend)],
            "month": [int(month)],
            "temperature": [float(temperature)],
            "humidity": [float(humidity)],
            "number_of_people": [int(number_of_people)],
            "appliance_usage_encoded": [int(app_encoded)],
            "previous_consumption": [float(previous_consumption)],
            "rolling_3h_avg": [float(rolling_3h_avg)]
        }

        X_input = pd.DataFrame(feature_dict)[FEATURE_COLUMNS]

        # ML Model Prediction
        raw_pred = self._model.predict(X_input)[0]
        pred_kwh = max(0.35, round(float(raw_pred), 2))

        # Financial Calculations
        estimated_cost = round(pred_kwh * tariff_per_kwh, 2)
        # Daily estimated projection (avg 24h factor ~ 20x hourly)
        est_daily_kwh = round(pred_kwh * 18.5, 1)
        est_daily_cost = round(est_daily_kwh * tariff_per_kwh, 2)
        est_monthly_kwh = round(est_daily_kwh * 30, 1)
        est_monthly_cost = round(est_monthly_kwh * tariff_per_kwh, 2)

        # Categorization
        if pred_kwh < 3.5:
            category = "Low"
            category_color = "success"
            category_badge = "Low Energy Usage"
            category_description = "Excellent! Your energy consumption is well within eco-friendly limits."
        elif pred_kwh <= 7.5:
            category = "Normal"
            category_color = "primary"
            category_badge = "Moderate Usage"
            category_description = "Standard consumption level. Minor optimizations can lower your utility bill."
        else:
            category = "High"
            category_color = "danger"
            category_badge = "High Consumption Alert"
            category_description = "High energy usage detected. Immediate optimization recommended to prevent tariff surge."

        # Dynamic Smart Optimization Tips
        recommendations = generate_smart_recommendations(
            hour=hour,
            temperature=temperature,
            humidity=humidity,
            people=number_of_people,
            appliance_level=app_clean,
            predicted_kwh=pred_kwh,
            tariff=tariff_per_kwh,
            currency=currency
        )

        return {
            "predicted_kwh": pred_kwh,
            "estimated_cost": estimated_cost,
            "est_daily_kwh": est_daily_kwh,
            "est_daily_cost": est_daily_cost,
            "est_monthly_kwh": est_monthly_kwh,
            "est_monthly_cost": est_monthly_cost,
            "currency": currency,
            "tariff": tariff_per_kwh,
            "category": category,
            "category_color": category_color,
            "category_badge": category_badge,
            "category_description": category_description,
            "recommendations": recommendations,
            "input_summary": {
                "date": date_str,
                "time": time_str,
                "hour": hour,
                "temperature": temperature,
                "humidity": humidity,
                "number_of_people": number_of_people,
                "appliance_usage": appliance_usage,
                "previous_consumption": previous_consumption
            }
        }

def load_trained_model(model_path: str = "models/energy_model.pkl"):
    """Loads and returns the singleton predictor instance."""
    return EnergyPredictor.get_instance(model_path)

def predict_energy_consumption(
    date: str,
    time: str,
    temperature: float,
    humidity: float,
    number_of_people: int,
    appliance_usage: str,
    previous_consumption: float,
    tariff_per_kwh: float = 8.0,
    currency: str = "₹",
    model_path: str = "models/energy_model.pkl"
) -> Dict[str, Any]:
    """Functional wrapper for single ML prediction."""
    predictor = EnergyPredictor.get_instance(model_path)
    return predictor.predict(
        date_str=date,
        time_str=time,
        temperature=temperature,
        humidity=humidity,
        number_of_people=number_of_people,
        appliance_usage=appliance_usage,
        previous_consumption=previous_consumption,
        tariff_per_kwh=tariff_per_kwh,
        currency=currency
    )
