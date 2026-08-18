"""
Automated Pytest Test Suite for AI Smart Energy Optimization System
Tests Authentication, Machine Learning, Preprocessing, Cost Calculation, and Routes.
"""

import os
import pytest
import pandas as pd
import numpy as np
from app import create_app
from config import Config
from models import db, User, EnergyRecord, Prediction
from ml.preprocessing import clean_dataset, prepare_features, validate_uploaded_csv, FEATURE_COLUMNS
from ml.train import train_energy_models
from ml.prediction import predict_energy_consumption
from ml.optimization import generate_smart_recommendations, EnergySavingSimulator
from routes.cost_calculator import calculate_tiered_cost

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    """Creates a test Flask application context with in-memory database."""
    test_app = create_app(TestConfig)
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Provides a test HTTP client."""
    return app.test_client()

def test_preprocessing_and_cleaning():
    """Verifies that missing values are imputed and features properly extracted."""
    sample_data = {
        "date": ["2024-06-01", "2024-06-01"],
        "time": ["08:00", "19:00"],
        "temperature": [np.nan, 32.0],
        "humidity": [60.0, np.nan],
        "number_of_people": [2, np.nan],
        "appliance_usage": ["low", "HIGH"],
        "energy_consumption": [3.5, 7.8]
    }
    df = pd.DataFrame(sample_data)
    cleaned = clean_dataset(df)
    
    assert not cleaned.empty
    assert cleaned["temperature"].isna().sum() == 0
    assert cleaned["humidity"].isna().sum() == 0
    assert cleaned["number_of_people"].isna().sum() == 0
    assert cleaned["appliance_usage_encoded"].iloc[0] == 1
    assert cleaned["appliance_usage_encoded"].iloc[1] == 3
    
    X, y = prepare_features(df)
    assert X.shape[1] == len(FEATURE_COLUMNS)
    assert y is not None
    assert len(y) == 2

def test_ml_prediction():
    """Verifies that the ML model produces valid predictions and costs."""
    res = predict_energy_consumption(
        date="2024-06-15",
        time="19:30",
        temperature=32.0,
        humidity=65.0,
        number_of_people=3,
        appliance_usage="High",
        previous_consumption=4.5,
        tariff_per_kwh=8.0,
        currency="₹"
    )
    
    assert "predicted_kwh" in res
    assert res["predicted_kwh"] > 0.0
    assert res["estimated_cost"] == round(res["predicted_kwh"] * 8.0, 2)
    assert res["category"] in ["Low", "Normal", "High"]
    assert len(res["recommendations"]) > 0

def test_cost_calculations():
    """Verifies flat and tiered slab electricity billing mathematics."""
    tiered = calculate_tiered_cost(monthly_kwh=250.0, base_tariff=8.0)
    
    # Tier 1: 100 kWh @ 4.8 = 480
    # Tier 2: 150 kWh @ 8.0 = 1200
    # Total = 1680
    assert tiered["tier1"]["cost"] == 480.0
    assert tiered["tier2"]["cost"] == 1200.0
    assert tiered["tier3"]["cost"] == 0.0
    assert tiered["total_cost"] == 1680.0

def test_energy_saving_simulator():
    """Verifies that simulator produces accurate savings calculations."""
    sim = EnergySavingSimulator.calculate_simulation(
        baseline_monthly_kwh=240.0,
        tariff_per_kwh=8.0,
        reduce_ac_pct=20.0,
        reduce_lighting_pct=20.0,
        reduce_appliances_pct=10.0,
        shift_peak_pct=20.0,
        eliminate_standby=True
    )
    
    assert sim["total_kwh_saved"] > 0.0
    assert sim["money_saved_monthly"] > 0.0
    assert sim["projected_monthly_kwh"] < 240.0
    assert sim["percentage_saved"] > 0.0

def test_user_auth_flow(client):
    """Verifies registration, login, protected route access, and logout."""
    # 1. Register a new user
    reg_response = client.post("/register", data={
        "name": "Test Student",
        "email": "test@student.edu",
        "password": "password123",
        "confirm_password": "password123",
        "currency": "₹",
        "tariff": "8.0"
    }, follow_redirects=True)
    
    assert reg_response.status_code == 200
    assert b"Test Student" in reg_response.data
    
    # 2. Access dashboard
    dash_response = client.get("/dashboard")
    assert dash_response.status_code == 200
    assert b"Dashboard" in dash_response.data
    
    # 3. Access prediction page
    pred_response = client.get("/predict")
    assert pred_response.status_code == 200
    
    # 4. Access Analytics
    analytics_response = client.get("/analytics")
    assert analytics_response.status_code == 200
    
    # 5. Access Optimization
    opt_response = client.get("/optimization")
    assert opt_response.status_code == 200
    
    # 6. Access Model Performance
    perf_response = client.get("/model-performance")
    assert perf_response.status_code == 200
    
    # 7. Access Cost Calculator
    calc_response = client.get("/cost-calculator")
    assert calc_response.status_code == 200
    
    # 8. Test AJAX Simulator endpoint
    sim_api_resp = client.post("/api/simulate-savings", json={
        "baseline_monthly_kwh": 250,
        "tariff": 8.0,
        "reduce_ac_pct": 15,
        "reduce_lighting_pct": 10,
        "reduce_appliances_pct": 10,
        "shift_peak_pct": 20,
        "eliminate_standby": True
    })
    assert sim_api_resp.status_code == 200
    sim_json = sim_api_resp.get_json()
    assert sim_json["success"] is True
    assert sim_json["data"]["total_kwh_saved"] > 0
    
    # 9. Logout
    logout_response = client.get("/logout", follow_redirects=True)
    assert logout_response.status_code == 200
    assert b"Sign In" in logout_response.data
    
    # 10. Access dashboard unauthenticated -> redirects to login
    unauth_response = client.get("/dashboard", follow_redirects=True)
    assert b"Please log in to access this page" in unauth_response.data

def test_csv_upload_validation(tmp_path):
    """Verifies that CSV validation handles empty and valid CSV files correctly."""
    # Empty CSV
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("")
    is_valid, msg, _, _ = validate_uploaded_csv(str(empty_csv))
    assert not is_valid
    
    # Valid CSV
    valid_csv = tmp_path / "valid.csv"
    valid_csv.write_text(
        "date,time,temperature,humidity,number_of_people,appliance_usage,previous_consumption,energy_consumption\n"
        "2024-06-01,12:00,30.0,60.0,2,Medium,3.5,4.2\n"
        "2024-06-01,13:00,31.0,58.0,2,Medium,4.2,4.5\n"
        "2024-06-01,14:00,32.0,55.0,2,Medium,4.5,4.8\n"
        "2024-06-01,15:00,31.5,57.0,2,Medium,4.8,4.6\n"
        "2024-06-01,16:00,30.5,59.0,2,Medium,4.6,4.3\n"
    )
    is_valid, msg, stats, cleaned_df = validate_uploaded_csv(str(valid_csv))
    assert is_valid
    assert stats["total_rows"] == 5
    assert cleaned_df is not None

def test_sample_csv_download(client):
    """Verifies that the sample CSV download route works."""
    res = client.get("/download-sample-csv")
    assert res.status_code == 200
    assert "text/csv" in res.content_type
    assert b"energy_consumption" in res.data
