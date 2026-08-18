"""
Flask Blueprints Registry
"""

from .auth import auth_bp
from .dashboard import dashboard_bp
from .prediction import prediction_bp
from .analytics import analytics_bp
from .optimization import optimization_bp
from .upload import upload_bp
from .model_performance import model_performance_bp
from .cost_calculator import cost_calculator_bp
from .history import history_bp
from .settings import settings_bp
from .about import about_bp

def register_blueprints(app):
    """Registers all application blueprint routes."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(optimization_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(model_performance_bp)
    app.register_blueprint(cost_calculator_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(about_bp)
