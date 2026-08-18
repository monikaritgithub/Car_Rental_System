"""
Configuration settings for the Smriti Car Rental System.

This module defines the base configuration and any environment-specific
overrides. Keeping configuration separate from application code makes it
easy to change settings without touching business logic.
"""

import os
from pathlib import Path

# The root of the project — two levels up from this file (config/settings.py)
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """
    Base configuration shared by both the customer and admin applications.

    Secret key is used by Flask for session signing and CSRF protection.
    It should never be hardcoded in a real production environment — use
    an environment variable instead. For this demonstration, we fall back
    to a fixed development key if none is set.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY", "smriti-car-rental-dev-key-2026")

    # SQLite database stored in the project root
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'car_rental.db'}"

    # Disabling modification tracking saves a small amount of memory
    # and suppresses a deprecation warning from SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Maximum upload size for car images (2MB)
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    # Where car images are stored on disk, relative to project root
    IMAGES_DIR = BASE_DIR / "images"

    # Minimum and maximum rental days enforced at the service layer
    # The car model also stores per-car limits, but these are system-wide guards
    SYSTEM_MIN_RENT_DAYS = 1
    SYSTEM_MAX_RENT_DAYS = 90


class DevelopmentConfig(Config):
    """Development configuration — enables Flask's debug mode."""
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configuration.

    Uses an in-memory SQLite database so tests run fast and don't
    touch the real database file.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key"


class ProductionConfig(Config):
    """Production configuration — debug off, stricter settings."""
    DEBUG = False
