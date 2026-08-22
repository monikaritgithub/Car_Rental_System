"""
Admin application factory.

Creates and configures the Flask app for the admin interface,
which runs on port 5001.
"""

from flask import Flask
from database import db
from config.settings import DevelopmentConfig


def create_admin_app(config_class=DevelopmentConfig) -> Flask:
    """
    Build the admin Flask application.

    This is a completely separate Flask instance from the customer app.
    They share the same SQLite database but have different routes,
    templates, and static assets.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    db.init_app(app)

    from app.admin_app.routes import admin_bp
    app.register_blueprint(admin_bp)

    return app
