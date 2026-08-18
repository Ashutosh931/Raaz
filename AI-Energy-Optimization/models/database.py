from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    """User account model with secure password hashing and relationship links."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    currency = db.Column(db.String(10), default="₹")
    default_tariff = db.Column(db.Float, default=8.0)  # INR per kWh
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    predictions = db.relationship("Prediction", backref="user", lazy=True, cascade="all, delete-orphan")
    energy_records = db.relationship("EnergyRecord", backref="user", lazy=True, cascade="all, delete-orphan")
    alerts = db.relationship("Alert", backref="user", lazy=True, cascade="all, delete-orphan")
    settings = db.relationship("UserSetting", backref="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password: str):
        """Hashes and sets user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifies given password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Prediction(db.Model):
    """Stores ML energy predictions made by the user."""
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    hour = db.Column(db.Integer, default=12)
    
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    people = db.Column(db.Integer, default=1)
    appliance_usage = db.Column(db.String(20), default="Medium")  # Low, Medium, High
    previous_consumption = db.Column(db.Float, nullable=False)
    
    predicted_consumption = db.Column(db.Float, nullable=False)  # in kWh
    estimated_cost = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), default="Normal")  # Low, Normal, High
    recommendations_json = db.Column(db.Text, nullable=True)  # JSON-encoded dynamic tips
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Prediction {self.id}: {self.predicted_consumption:.2f} kWh>"


class EnergyRecord(db.Model):
    """Historical or uploaded energy consumption records."""
    __tablename__ = "energy_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    date = db.Column(db.String(20), nullable=False, index=True)
    time = db.Column(db.String(10), default="00:00")
    hour = db.Column(db.Integer, default=0)
    
    consumption = db.Column(db.Float, nullable=False)  # in kWh
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    people = db.Column(db.Integer, default=1)
    appliance = db.Column(db.String(50), default="All Appliances")
    cost = db.Column(db.Float, default=0.0)
    
    source = db.Column(db.String(30), default="manual")  # 'manual', 'upload', 'synthetic'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EnergyRecord {self.id}: {self.date} {self.consumption:.2f} kWh>"


class Alert(db.Model):
    """Energy alerts and notification items for users."""
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    alert_type = db.Column(db.String(20), default="info")  # info, warning, critical, success
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Alert {self.alert_type}: {self.title}>"


class UserSetting(db.Model):
    """User preferences including theme, custom alerts, and default tariff rates."""
    __tablename__ = "user_settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    
    dark_mode = db.Column(db.Boolean, default=False)
    default_tariff = db.Column(db.Float, default=8.0)
    currency = db.Column(db.String(10), default="₹")
    alert_threshold_kwh = db.Column(db.Float, default=8.0)
    peak_hour_start = db.Column(db.Integer, default=18)
    peak_hour_end = db.Column(db.Integer, default=22)

    def __repr__(self):
        return f"<UserSetting user_id={self.user_id}>"
