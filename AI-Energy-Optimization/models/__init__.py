from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .database import User, Prediction, EnergyRecord, Alert, UserSetting
