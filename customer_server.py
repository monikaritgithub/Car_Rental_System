"""
Customer server entry point.

Run this file to start the customer-facing web application on port 5000:
    .venv\Scripts\python customer_server.py

The database tables are created automatically on first run if they don't
already exist. This makes it easy to start fresh without a separate setup step.
"""

import sys
import os

# Make sure the project root is on the Python path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.customer_app import create_customer_app
from app.models import Customer, Admin, Car, Booking, Payment
from database import db


def main():
    app = create_customer_app()

    with app.app_context():
        # Create all tables if they don't exist yet.
        # SQLAlchemy checks the schema and only creates missing tables —
        # it won't overwrite existing data.
        db.create_all()
        print("Database tables ready.")

    print("Starting Customer application on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)


if __name__ == "__main__":
    main()
