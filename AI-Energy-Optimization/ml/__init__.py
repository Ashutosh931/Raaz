"""
Machine Learning module for Energy Consumption Prediction and Optimization.
"""

from .preprocessing import prepare_features, clean_dataset, FEATURE_COLUMNS
from .train import train_energy_models, evaluate_models
from .prediction import predict_energy_consumption, load_trained_model, EnergyPredictor
from .optimization import generate_smart_recommendations, EnergySavingSimulator
