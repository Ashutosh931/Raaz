"""
Data Preprocessing and Feature Engineering for Energy Consumption Prediction.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, Optional

FEATURE_COLUMNS = [
    "hour",
    "day_of_week",
    "is_weekend",
    "month",
    "temperature",
    "humidity",
    "number_of_people",
    "appliance_usage_encoded",
    "previous_consumption",
    "rolling_3h_avg"
]

TARGET_COLUMN = "energy_consumption"

APPLIANCE_MAPPING = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "1": 1,
    "2": 2,
    "3": 3,
    1: 1,
    2: 2,
    3: 3
}

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw or uploaded dataset:
    - Converts date/time columns to datetime features
    - Imputes missing numerical values
    - Standardizes appliance usage categorical labels
    - Calculates lag/rolling features if missing
    - Removes invalid/negative rows
    """
    df = df.copy()
    
    # 1. Normalize column names (lowercase, stripped, replace spaces with underscores)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    # 2. Handle Date/Time extraction
    if "date" in df.columns:
        try:
            df["parsed_date"] = pd.to_datetime(df["date"], errors="coerce")
            if "day" not in df.columns:
                df["day"] = df["parsed_date"].dt.day.fillna(15).astype(int)
            if "month" not in df.columns:
                df["month"] = df["parsed_date"].dt.month.fillna(6).astype(int)
            if "day_of_week" not in df.columns:
                df["day_of_week"] = df["parsed_date"].dt.dayofweek.fillna(2).astype(int)
        except Exception:
            pass

    # If datetime or timestamp column exists
    for dt_col in ["datetime", "timestamp"]:
        if dt_col in df.columns:
            try:
                parsed = pd.to_datetime(df[dt_col], errors="coerce")
                df["hour"] = parsed.dt.hour.fillna(12).astype(int)
                df["day"] = parsed.dt.day.fillna(15).astype(int)
                df["month"] = parsed.dt.month.fillna(6).astype(int)
                df["day_of_week"] = parsed.dt.dayofweek.fillna(2).astype(int)
            except Exception:
                pass

    if "time" in df.columns and "hour" not in df.columns:
        try:
            df["hour"] = pd.to_datetime(df["time"], format="%H:%M", errors="coerce").dt.hour.fillna(12).astype(int)
        except Exception:
            df["hour"] = 12

    # Default missing time fields
    if "hour" not in df.columns:
        df["hour"] = 12
    else:
        df["hour"] = pd.to_numeric(df["hour"], errors="coerce").fillna(12).astype(int).clip(0, 23)

    if "day_of_week" not in df.columns:
        df["day_of_week"] = 2  # Wednesday default
    else:
        df["day_of_week"] = pd.to_numeric(df["day_of_week"], errors="coerce").fillna(2).astype(int).clip(0, 6)

    if "is_weekend" not in df.columns:
        df["is_weekend"] = df["day_of_week"].apply(lambda x: 1 if x in [5, 6] else 0)
    else:
        df["is_weekend"] = pd.to_numeric(df["is_weekend"], errors="coerce").fillna(0).astype(int)

    if "month" not in df.columns:
        df["month"] = 6
    else:
        df["month"] = pd.to_numeric(df["month"], errors="coerce").fillna(6).astype(int).clip(1, 12)

    # 3. Ambient Weather Features
    if "temperature" not in df.columns:
        df["temperature"] = 28.0
    else:
        df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
        df["temperature"] = df["temperature"].fillna(df["temperature"].median() if not df["temperature"].isna().all() else 28.0)
        df["temperature"] = df["temperature"].clip(0.0, 55.0)

    if "humidity" not in df.columns:
        df["humidity"] = 55.0
    else:
        df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
        df["humidity"] = df["humidity"].fillna(df["humidity"].median() if not df["humidity"].isna().all() else 55.0)
        df["humidity"] = df["humidity"].clip(10.0, 100.0)

    # 4. Occupancy
    people_col = None
    for candidate in ["number_of_people", "people", "occupants", "occupancy"]:
        if candidate in df.columns:
            people_col = candidate
            break
    if people_col:
        df["number_of_people"] = pd.to_numeric(df[people_col], errors="coerce").fillna(2).astype(int).clip(1, 20)
    else:
        df["number_of_people"] = 2

    # 5. Appliance Usage Encoding
    app_col = None
    for candidate in ["appliance_usage", "appliance_level", "appliance_usage_level"]:
        if candidate in df.columns:
            app_col = candidate
            break

    if app_col:
        df["appliance_usage_encoded"] = df[app_col].astype(str).str.strip().str.lower().map(APPLIANCE_MAPPING).fillna(2).astype(int)
    elif "appliance_usage_encoded" not in df.columns:
        df["appliance_usage_encoded"] = 2

    # 6. Target & Lag Features
    target_candidate = None
    for candidate in ["energy_consumption", "consumption", "kwh", "power_consumption", "energy_kwh"]:
        if candidate in df.columns:
            target_candidate = candidate
            break

    if target_candidate and target_candidate != TARGET_COLUMN:
        df[TARGET_COLUMN] = pd.to_numeric(df[target_candidate], errors="coerce")
    elif TARGET_COLUMN in df.columns:
        df[TARGET_COLUMN] = pd.to_numeric(df[TARGET_COLUMN], errors="coerce")

    # Clean target
    if TARGET_COLUMN in df.columns:
        df = df[df[TARGET_COLUMN] > 0]
        df[TARGET_COLUMN] = df[TARGET_COLUMN].fillna(df[TARGET_COLUMN].median())

    # Calculate previous_consumption & rolling_3h_avg if missing
    if "previous_consumption" not in df.columns:
        if TARGET_COLUMN in df.columns:
            df["previous_consumption"] = df[TARGET_COLUMN].shift(1).bfill()
        else:
            df["previous_consumption"] = 2.5
    else:
        df["previous_consumption"] = pd.to_numeric(df["previous_consumption"], errors="coerce")
        df["previous_consumption"] = df["previous_consumption"].fillna(2.5).clip(lower=0.1)

    if "rolling_3h_avg" not in df.columns:
        if TARGET_COLUMN in df.columns:
            df["rolling_3h_avg"] = df[TARGET_COLUMN].rolling(window=3, min_periods=1).mean().bfill()
        else:
            df["rolling_3h_avg"] = df["previous_consumption"]
    else:
        df["rolling_3h_avg"] = pd.to_numeric(df["rolling_3h_avg"], errors="coerce")
        df["rolling_3h_avg"] = df["rolling_3h_avg"].fillna(df["previous_consumption"]).clip(lower=0.1)

    return df

def prepare_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
    """
    Extracts standard X feature matrix and y target vector.
    """
    cleaned_df = clean_dataset(df)
    X = cleaned_df[FEATURE_COLUMNS]
    y = cleaned_df[TARGET_COLUMN] if TARGET_COLUMN in cleaned_df.columns else None
    return X, y

def validate_uploaded_csv(file_path: str) -> Tuple[bool, str, Optional[Dict[str, Any]], Optional[pd.DataFrame]]:
    """
    Validates user-uploaded CSV file for energy analysis and ML training/prediction.
    
    Returns:
    - is_valid (bool)
    - message (str)
    - statistics (dict)
    - cleaned_df (pd.DataFrame)
    """
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            return False, "The uploaded CSV file is empty.", None, None
            
        if len(df) < 5:
            return False, f"The CSV contains only {len(df)} rows. Please provide at least 5 records.", None, None
            
        cleaned_df = clean_dataset(df)
        
        # Calculate summary statistics
        total_rows = len(cleaned_df)
        has_target = TARGET_COLUMN in cleaned_df.columns
        
        stats = {
            "total_rows": total_rows,
            "columns": list(cleaned_df.columns),
            "feature_columns": FEATURE_COLUMNS,
            "has_target": has_target,
            "avg_temperature": round(float(cleaned_df["temperature"].mean()), 1) if "temperature" in cleaned_df.columns else 0.0,
            "avg_humidity": round(float(cleaned_df["humidity"].mean()), 1) if "humidity" in cleaned_df.columns else 0.0,
            "total_energy": round(float(cleaned_df[TARGET_COLUMN].sum()), 2) if has_target else 0.0,
            "avg_energy": round(float(cleaned_df[TARGET_COLUMN].mean()), 2) if has_target else 0.0,
            "max_energy": round(float(cleaned_df[TARGET_COLUMN].max()), 2) if has_target else 0.0,
            "min_energy": round(float(cleaned_df[TARGET_COLUMN].min()), 2) if has_target else 0.0,
            "missing_values_imputed": int(df.isna().sum().sum()),
            "preview_data": cleaned_df.head(10).to_dict(orient="records")
        }
        
        return True, "Dataset successfully validated and cleaned.", stats, cleaned_df
        
    except Exception as e:
        return False, f"Error processing CSV: {str(e)}", None, None
