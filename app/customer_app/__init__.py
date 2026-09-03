"""
Customer application factory.

Creates and configures the Flask app for the customer-facing interface,
which runs on port 5000.
"""

from flask import Flask

from config.settings import Config, DevelopmentConfig
from database import db


def create_customer_app(config_class: type[Config] = DevelopmentConfig) -> Flask:
    """
    Build the customer Flask application.

    Using an application factory (this function) rather than a global app
    object makes it easy to create separate instances for testing.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    # Bind the SQLAlchemy instance to this app
    db.init_app(app)

    # Register the customer blueprints (routes)
    from app.customer_app.routes import customer_bp
    app.register_blueprint(customer_bp)

    return app
