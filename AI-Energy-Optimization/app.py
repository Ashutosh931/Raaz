"""
AI-Based Smart Energy Consumption Prediction and Optimization System
Main Flask Application Entrypoint
"""

import os
from flask import Flask, render_template, session
from config import Config
from models import db, User, UserSetting, Alert
from routes import register_blueprints
from ml.prediction import EnergyPredictor

def create_app(config_class=Config):
    """Application Factory Pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    base_dir = app.config.get("BASE_DIR", Config.BASE_DIR)
    os.makedirs(os.path.join(base_dir, "database"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "data", "uploads"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "models"), exist_ok=True)

    # Initialize SQLite Database with SQLAlchemy
    db.init_app(app)

    # Register Route Blueprints
    register_blueprints(app)

    # Context Processors for Templates
    @app.context_processor
    def inject_global_context():
        """Injects user details, theme preference, and currency across all templates."""
        user_info = None
        user_theme = "light"
        user_currency = "₹"
        unread_alerts_count = 0

        if "user_id" in session:
            try:
                user = db.session.get(User, session["user_id"])
                if user:
                    user_info = user
                    user_currency = user.currency
                    if user.settings:
                        user_theme = "dark" if user.settings.dark_mode else "light"
                    unread_alerts_count = Alert.query.filter_by(user_id=user.id, is_read=False).count()
            except Exception:
                pass

        return {
            "current_user": user_info,
            "user_theme": user_theme,
            "global_currency": user_currency,
            "unread_alerts_count": unread_alerts_count,
            "app_name": "SmartEnergy AI"
        }

    # Custom Jinja Filters
    @app.template_filter("currency_format")
    def currency_filter(amount, symbol="₹"):
        try:
            return f"{symbol}{float(amount):,.2f}"
        except (ValueError, TypeError):
            return f"{symbol}0.00"

    @app.template_filter("kwh_format")
    def kwh_filter(value):
        try:
            return f"{float(value):,.2f} kWh"
        except (ValueError, TypeError):
            return "0.00 kWh"

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("base.html", error_title="Page Not Found", error_message="The requested page does not exist."), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("base.html", error_title="Internal Server Error", error_message="An unexpected server error occurred. Please try again."), 500

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return render_template("base.html", error_title="File Too Large", error_message="The uploaded CSV file exceeds the 16MB limit."), 413

    # Initialize Database Tables & Model Loader inside app context
    with app.app_context():
        db.create_all()
        
        # Check and initialize ML model artifact in background
        try:
            model_path = app.config.get("MODEL_PATH", Config.MODEL_PATH)
            dataset_path = app.config.get("DATASET_PATH", Config.DATASET_PATH)
            if not os.path.exists(dataset_path):
                from generate_dataset import generate_energy_dataset
                generate_energy_dataset(output_path=dataset_path)
            if not os.path.exists(model_path):
                from ml.train import train_energy_models
                train_energy_models(dataset_path=dataset_path, model_save_path=model_path)
            EnergyPredictor.get_instance(model_path)
        except Exception as e:
            print(f"[!] Warning during startup model initialization: {e}")

    return app

app = create_app()

if __name__ == "__main__":
    print("=" * 65)
    print(" AI-Based Smart Energy Consumption Prediction & Optimization")
    print(" Server Starting on http://127.0.0.1:5000")
    print("=" * 65)
    app.run(host="0.0.0.0", port=5000, debug=True)
