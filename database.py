"""
Database initialization for the Smriti Car Rental System.

This module creates the shared SQLAlchemy instance used by all models.
Keeping it here (rather than inside app/) prevents circular import problems
when models import from each other.
"""

from flask_sqlalchemy import SQLAlchemy

# This db object is imported by every model and by the app factories.
# It is intentionally created here without binding it to a specific app —
# Flask-SQLAlchemy supports this pattern (sometimes called the "application factory" pattern).
db = SQLAlchemy()
