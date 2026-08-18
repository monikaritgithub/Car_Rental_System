"""
Admin server entry point.

Run this file to start the admin interface on port 5001:
    .venv\Scripts\python admin_server.py

The customer and admin servers both connect to the same SQLite database
file (car_rental.db) so they see the same data in real time.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.admin_app import create_admin_app
from app.models import Customer, Admin, Car, Booking, Payment
from database import db


def main():
    app = create_admin_app()

    with app.app_context():
        db.create_all()
        print("Database tables ready.")

    print("Starting Admin application on http://127.0.0.1:5001")
    app.run(host="127.0.0.1", port=5001, debug=True, use_reloader=False)


if __name__ == "__main__":
    main()
