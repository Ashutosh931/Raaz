"""
Standalone CLI Prediction Demonstration Script
Usage:
    python predict.py
"""

import sys
import os
from datetime import datetime

# Configure UTF-8 stdout if possible on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ml.prediction import predict_energy_consumption

def main():
    print("=" * 65)
    print(" AI-Based Smart Energy Consumption Prediction - CLI Demo")
    print("=" * 65)
    
    # Default test inputs
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = "19:30"
    temp = 32.5
    humidity = 68.0
    people = 4
    appliance_usage = "High"
    prev_kwh = 5.2
    tariff = 8.0
    
    print("Input Parameters:")
    print(f"  * Date & Time          : {date_str} {time_str} (Evening Peak)")
    print(f"  * Temperature          : {temp} C")
    print(f"  * Humidity             : {humidity} %")
    print(f"  * Occupancy            : {people} People")
    print(f"  * Appliance Usage Level: {appliance_usage}")
    print(f"  * Previous Consumption : {prev_kwh} kWh")
    print(f"  * Electricity Tariff   : INR {tariff}/kWh")
    print("-" * 65)
    
    try:
        result = predict_energy_consumption(
            date=date_str,
            time=time_str,
            temperature=temp,
            humidity=humidity,
            number_of_people=people,
            appliance_usage=appliance_usage,
            previous_consumption=prev_kwh,
            tariff_per_kwh=tariff,
            currency="₹"
        )
        
        print("\n PREDICTION RESULTS:")
        print(f"  * Predicted Consumption : {result['predicted_kwh']} kWh")
        print(f"  * Estimated Hourly Cost : INR {result['estimated_cost']}")
        print(f"  * Estimated Daily Usage : {result['est_daily_kwh']} kWh (INR {result['est_daily_cost']})")
        print(f"  * Estimated Monthly Bill: INR {result['est_monthly_cost']} ({result['est_monthly_kwh']} kWh)")
        print(f"  * Category              : [{result['category']}] - {result['category_badge']}")
        print(f"  * Assessment            : {result['category_description']}")
        
        print("\n SMART OPTIMIZATION RECOMMENDATIONS:")
        for idx, rec in enumerate(result["recommendations"][:3], 1):
            print(f"  {idx}. {rec['title']}")
            print(f"     -> Action: {rec['action']}")
            print(f"     -> Est. Monthly Saving: INR {rec['money_saved_monthly']} ({rec['kwh_saved_monthly']} kWh)")
            
        print("\n" + "=" * 65)
        
    except Exception as e:
        print(f"[ERROR] Prediction failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
