"""
Synthetic Energy Consumption Dataset Generator
Generates realistic, physically-grounded residential electricity consumption data
for training Machine Learning prediction models.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_energy_dataset(num_days: int = 180, output_path: str = "data/energy_consumption.csv") -> str:
    """
    Generates realistic hourly electricity consumption time-series data.
    
    Features generated:
    - date, time, hour, day, month, day_of_week, is_weekend
    - temperature (°C), humidity (%)
    - number_of_people
    - appliance_usage (Low, Medium, High)
    - previous_consumption (kWh)
    - rolling_3h_avg (kWh)
    - energy_consumption (Target in kWh)
    - appliance breakdown (AC, Refrigerator, Lighting, Laundry, Others)
    """
    print(f"Generating realistic energy consumption dataset for {num_days} days...")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    start_date = datetime(2024, 1, 1, 0, 0)
    total_hours = num_days * 24
    
    np.random.seed(42)
    random.seed(42)
    
    records = []
    prev_consumption = 1.2
    recent_history = [1.2, 1.3, 1.1]
    
    for h_idx in range(total_hours):
        current_dt = start_date + timedelta(hours=h_idx)
        
        date_str = current_dt.strftime("%Y-%m-%d")
        time_str = current_dt.strftime("%H:%M")
        hour = current_dt.hour
        day = current_dt.day
        month = current_dt.month
        day_of_week = current_dt.weekday() # 0 = Monday, 6 = Sunday
        is_weekend = 1 if day_of_week in [5, 6] else 0
        
        # 1. Temperature Simulation (°C)
        # Seasonal base (colder in Jan/Feb, peak in May/Jun)
        season_temp_base = 20.0 + 12.0 * np.sin((month - 1) / 12.0 * 2 * np.pi - np.pi / 2)
        # Diurnal temperature cycle: peak around 14:00 (2 PM), coolest at 05:00
        diurnal_temp_var = 6.0 * np.sin((hour - 8) / 24.0 * 2 * np.pi)
        temperature = round(float(season_temp_base + diurnal_temp_var + np.random.normal(0, 1.2)), 1)
        temperature = max(10.0, min(45.0, temperature))
        
        # 2. Humidity Simulation (%) - inversely related to temperature
        humidity_base = 65.0 - (temperature - 25.0) * 1.2
        humidity = round(float(humidity_base + np.random.normal(0, 4.0)), 1)
        humidity = max(20.0, min(95.0, humidity))
        
        # 3. Occupancy Simulation
        # During weekday working hours (9 AM - 5 PM), fewer people at home
        if is_weekend:
            occupancy_prob = [0.05, 0.15, 0.35, 0.30, 0.15] # 1 to 5 people
        else:
            if 9 <= hour <= 17:
                occupancy_prob = [0.60, 0.25, 0.10, 0.05, 0.00]
            else:
                occupancy_prob = [0.10, 0.25, 0.35, 0.20, 0.10]
        number_of_people = int(np.random.choice([1, 2, 3, 4, 5], p=occupancy_prob))
        
        # 4. Appliance Usage Category
        # Peak evening hours (18 to 22) usually have higher appliance usage
        if 18 <= hour <= 22:
            usage_cat = np.random.choice(["Low", "Medium", "High"], p=[0.10, 0.35, 0.55])
        elif 7 <= hour <= 9:
            usage_cat = np.random.choice(["Low", "Medium", "High"], p=[0.20, 0.50, 0.30])
        elif 0 <= hour <= 5:
            usage_cat = "Low"
        else:
            usage_cat = np.random.choice(["Low", "Medium", "High"], p=[0.40, 0.45, 0.15])
            
        appliance_multiplier = {"Low": 0.85, "Medium": 1.15, "High": 1.55}[usage_cat]
        
        # 5. Energy Consumption Physics Model (kWh)
        # Base standby load (refrigerator, wifi, clocks, vampire draw)
        base_load = 0.45 + 0.05 * np.random.uniform(0.8, 1.2)
        
        # Occupant activity contribution
        occupant_load = 0.25 * number_of_people
        
        # Hourly activity profile
        if 0 <= hour <= 5:       # Late Night / Sleep
            activity_profile = 0.3
        elif 6 <= hour <= 8:     # Morning Wake-up
            activity_profile = 2.2
        elif 9 <= hour <= 16:    # Daytime
            activity_profile = 1.6 if is_weekend else 0.8
        elif 17 <= hour <= 21:   # Evening Peak (TV, Cooking, Lights, AC)
            activity_profile = 3.8
        else:                    # 22-23 Night
            activity_profile = 1.4
            
        # Cooling / Heating Load (HVAC)
        hvac_load = 0.0
        if temperature > 26.0:
            # AC consumption scales non-linearly with heat
            hvac_load = 0.18 * ((temperature - 26.0) ** 1.3) * (1.2 if 13 <= hour <= 23 else 0.8)
        elif temperature < 16.0:
            # Space heating
            hvac_load = 0.12 * (16.0 - temperature)
            
        # Humidity penalty on AC
        if humidity > 70.0 and temperature > 28.0:
            hvac_load += 0.35
            
        raw_consumption = (base_load + occupant_load + activity_profile + hvac_load) * appliance_multiplier
        
        # Blend with autoregressive previous consumption and noise
        consumption = 0.25 * prev_consumption + 0.75 * raw_consumption + np.random.normal(0, 0.18)
        consumption = max(0.4, round(float(consumption), 2))
        
        rolling_avg = round(float(np.mean(recent_history)), 2)
        
        # Estimate appliance breakdown (for realistic dashboard visualization)
        ac_kwh = round(max(0.0, float(hvac_load * 0.75 * appliance_multiplier)), 2)
        fridge_kwh = round(float(0.18 + np.random.uniform(0.01, 0.04)), 2)
        lighting_kwh = round(float(0.08 + (0.45 if (18 <= hour <= 23) else 0.05) * number_of_people * 0.15), 2)
        laundry_kwh = round(float(0.85 if (usage_cat == "High" and (hour in [10, 11, 19, 20])) else 0.0), 2)
        other_kwh = round(max(0.1, float(consumption - (ac_kwh + fridge_kwh + lighting_kwh + laundry_kwh))), 2)
        
        records.append({
            "date": date_str,
            "time": time_str,
            "hour": hour,
            "day": day,
            "month": month,
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "temperature": temperature,
            "humidity": humidity,
            "number_of_people": number_of_people,
            "appliance_usage": usage_cat,
            "previous_consumption": prev_consumption,
            "rolling_3h_avg": rolling_avg,
            "ac_consumption": ac_kwh,
            "refrigerator_consumption": fridge_kwh,
            "lighting_consumption": lighting_kwh,
            "laundry_consumption": laundry_kwh,
            "other_consumption": other_kwh,
            "energy_consumption": consumption
        })
        
        prev_consumption = consumption
        recent_history.append(consumption)
        if len(recent_history) > 3:
            recent_history.pop(0)
            
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} rows of synthetic energy data at '{output_path}'.")
    return output_path

if __name__ == "__main__":
    generate_energy_dataset()
