"""
Model Training and Evaluation Engine for Energy Consumption Prediction.
Trains Random Forest Regressor and benchmarks against Linear Regression.
"""

import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Dict, Any

from .preprocessing import prepare_features, FEATURE_COLUMNS, TARGET_COLUMN

def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculates standard regression performance metrics."""
    mae = float(mean_absolute_error(y_true, y_pred))
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_true, y_pred))
    
    return {
        "mae": round(mae, 4),
        "mse": round(mse, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4),
        "accuracy_pct": round(max(0.0, r2 * 100.0), 2)
    }

def train_energy_models(
    dataset_path: str = "data/energy_consumption.csv",
    model_save_path: str = "models/energy_model.pkl"
) -> Dict[str, Any]:
    """
    Loads dataset, trains Random Forest & Linear Regression, evaluates performance,
    calculates feature importances, and saves the trained pipeline.
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at '{dataset_path}'. Run generate_dataset.py first.")
        
    print(f"Loading dataset from: {dataset_path}")
    raw_df = pd.read_csv(dataset_path)
    
    X, y = prepare_features(raw_df)
    
    if y is None or len(y) == 0:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found or empty in dataset.")
        
    print(f"Dataset Shape: {X.shape[0]} rows, {X.shape[1]} features.")
    
    # 80/20 Train-Test split with reproducible seed
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    
    # 1. Train Random Forest Regressor (Primary Explainable Model)
    print("Training Random Forest Regressor...")
    rf_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=14,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_metrics = evaluate_predictions(y_test.values, rf_pred)
    
    # 2. Train Linear Regression (Academic Baseline Comparison)
    print("Training Linear Regression Baseline...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_metrics = evaluate_predictions(y_test.values, lr_pred)
    
    # 3. Extract Feature Importance for Explainability
    importances = rf_model.feature_importances_
    total_importance = np.sum(importances)
    
    feature_importance_list = []
    for feature_name, imp in sorted(zip(FEATURE_COLUMNS, importances), key=lambda x: x[1], reverse=True):
        pct = round((imp / total_importance) * 100.0, 2)
        feature_importance_list.append({
            "feature": feature_name,
            "label": feature_name.replace("_", " ").title(),
            "importance": round(float(imp), 4),
            "percentage": pct
        })
        
    # 4. Generate comparison sample for frontend charts (first 30 test records)
    test_sample_indices = np.arange(min(30, len(y_test)))
    comparison_sample = []
    y_test_array = y_test.values
    
    for idx in test_sample_indices:
        comparison_sample.append({
            "sample_index": int(idx + 1),
            "actual": round(float(y_test_array[idx]), 2),
            "rf_predicted": round(float(rf_pred[idx]), 2),
            "lr_predicted": round(float(lr_pred[idx]), 2),
            "error_rf": round(float(abs(y_test_array[idx] - rf_pred[idx])), 2)
        })
        
    # 5. Model Package Metadata
    model_artifact = {
        "model": rf_model,
        "linear_model": lr_model,
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "rf_metrics": rf_metrics,
        "lr_metrics": lr_metrics,
        "feature_importances": feature_importance_list,
        "comparison_sample": comparison_sample,
        "trained_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_samples": int(len(X)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test))
    }
    
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump(model_artifact, model_save_path)
    print(f"Model successfully saved to '{model_save_path}'.")
    print(f"Random Forest Performance: R2={rf_metrics['r2']:.4f}, MAE={rf_metrics['mae']:.4f} kWh, RMSE={rf_metrics['rmse']:.4f} kWh")
    print(f"Linear Regression Performance: R2={lr_metrics['r2']:.4f}, MAE={lr_metrics['mae']:.4f} kWh, RMSE={lr_metrics['rmse']:.4f} kWh")
    
    return model_artifact

def evaluate_models(model_save_path: str = "models/energy_model.pkl") -> Dict[str, Any]:
    """Loads saved model metadata and metrics."""
    if not os.path.exists(model_save_path):
        raise FileNotFoundError("Model file not found. Train the model first.")
    return joblib.load(model_save_path)
