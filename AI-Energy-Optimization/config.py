import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Application configuration settings."""
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.environ.get("SECRET_KEY", "ai-smart-energy-secret-key-2026-secure-viva-ready")
    
    # Database
    DB_DIR = os.path.join(BASE_DIR, "database")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(DB_DIR, 'energy.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Paths
    DATA_DIR = os.path.join(BASE_DIR, "data")
    UPLOAD_FOLDER = os.path.join(DATA_DIR, "uploads")
    DATASET_PATH = os.path.join(DATA_DIR, "energy_consumption.csv")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    MODEL_PATH = os.path.join(MODELS_DIR, "energy_model.pkl")
    
    # Limits & Defaults
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {"csv"}
    
    DEFAULT_CURRENCY = "₹"
    DEFAULT_TARIFF_PER_KWH = 8.00  # INR per kWh
    
    # Thresholds for Energy Alerts
    LOW_CONSUMPTION_THRESHOLD = 3.5    # kWh/hr
    HIGH_CONSUMPTION_THRESHOLD = 8.0   # kWh/hr
    CRITICAL_CONSUMPTION_THRESHOLD = 12.0 # kWh/hr
    
    # Peak Usage Hours (24-hour format)
    PEAK_HOURS_START = 18  # 6:00 PM
    PEAK_HOURS_END = 22    # 10:00 PM
