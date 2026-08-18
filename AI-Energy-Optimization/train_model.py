"""
Standalone Script to Train and Evaluate the ML Energy Prediction Model.
Usage:
    python train_model.py
"""

import sys
import os

# Configure UTF-8 stdout if possible on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ml.train import train_energy_models

def main():
    print("=" * 65)
    print(" AI-Based Smart Energy Consumption Prediction System")
    print(" Model Training & Benchmark Pipeline")
    print("=" * 65)
    
    dataset_path = os.path.join("data", "energy_consumption.csv")
    model_path = os.path.join("models", "energy_model.pkl")
    
    if not os.path.exists(dataset_path):
        print(f"[!] Dataset not found at '{dataset_path}'.")
        print("[*] Generating dataset now via generate_dataset.py...")
        from generate_dataset import generate_energy_dataset
        generate_energy_dataset(output_path=dataset_path)
        
    try:
        artifact = train_energy_models(dataset_path=dataset_path, model_save_path=model_path)
        rf_m = artifact["rf_metrics"]
        lr_m = artifact["lr_metrics"]
        
        print("\n" + "-" * 40)
        print(" TRAINING & EVALUATION COMPLETE")
        print("-" * 40)
        print("Random Forest (Primary Model):")
        print(f"  * R2 Score (Variance Explained): {rf_m['r2'] * 100:.2f}% (R2 = {rf_m['r2']:.4f})")
        print(f"  * Mean Absolute Error (MAE)    : {rf_m['mae']:.4f} kWh")
        print(f"  * Root Mean Squared Error (RMSE): {rf_m['rmse']:.4f} kWh")
        print("\nLinear Regression (Baseline Comparison):")
        print(f"  * R2 Score (Variance Explained): {lr_m['r2'] * 100:.2f}% (R2 = {lr_m['r2']:.4f})")
        print(f"  * Mean Absolute Error (MAE)    : {lr_m['mae']:.4f} kWh")
        print(f"  * Root Mean Squared Error (RMSE): {lr_m['rmse']:.4f} kWh")
        
        print("\nTop 5 Most Important Features for Prediction:")
        for idx, item in enumerate(artifact["feature_importances"][:5], 1):
            print(f"  {idx}. {item['label']:<24} -> {item['percentage']:>5.2f}%")
            
        print("\nModel saved successfully at:", model_path)
        print("=" * 65)
        
    except Exception as e:
        print(f"\n[ERROR] Model training failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
