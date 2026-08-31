"""
Database initialization and seed data script.

Run this to create all database tables and populate them with sample data:
    .venv\Scripts\python scripts\seed_data.py

The script is safe to run multiple times — it checks for existing data
before inserting, so it won't create duplicates.

Seed data includes:
  - One default admin account
  - Eight sample cars covering different categories
  - Two sample customers for testing
"""

import sys
import os

# Add the project root to the path so we can import from app/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.customer_app import create_customer_app
from app.models import Customer, Admin, Car, Booking, Payment
from database import db


def seed_database():
    """Create tables and insert seed data."""

    app = create_customer_app()

    with app.app_context():
        # Create all tables based on the model definitions
        db.create_all()
        print("Database tables created.")

        # ── Admin accounts ──────────────────────────────────────────────────

        if not db.session.query(Admin).first():
            admin = Admin(
                employee_id="EMP-001",
                department="Fleet Management",
                name="Smriti Bhandari",
                email="admin@smriticars.com"
            )
            admin.set_password("admin123")
            db.session.add(admin)
            print("Default admin account created: admin@smriticars.com / admin123")
        else:
            print("Admin accounts already exist, skipping.")

        # ── Sample customers ────────────────────────────────────────────────

        if not db.session.query(Customer).first():
            customers = [
                {
                    "name": "James Patel",
                    "email": "james@example.com",
                    "password": "customer123",
                    "phone_no": "021-555-0101",
                    "license_id_no": "LIC-NZ-00123",
                    "address": "12 Queens Drive, Wellington"
                },
                {
                    "name": "Aiko Tanaka",
                    "email": "aiko@example.com",
                    "password": "customer123",
                    "phone_no": "021-555-0202",
                    "license_id_no": "LIC-NZ-00456",
                    "address": "88 Ponsonby Road, Auckland"
                }
            ]

            for c_data in customers:
                c = Customer(
                    name=c_data["name"],
                    email=c_data["email"],
                    phone_no=c_data["phone_no"],
                    license_id_no=c_data["license_id_no"],
                    address=c_data["address"]
                )
                c.set_password(c_data["password"])
                db.session.add(c)

            print("Sample customer accounts created.")
        else:
            print("Customer accounts already exist, skipping.")

        # ── Car fleet ───────────────────────────────────────────────────────

        if not db.session.query(Car).first():
            cars = [
                {
                    "car_id": "CAR-001",
                    "make": "Toyota",
                    "model": "Camry",
                    "year": 2023,
                    "mileage": 12500.0,
                    "available_now": True,
                    "min_rent_period": 1,
                    "max_rent_period": 30,
                    "daily_rate": 75.0,
                    "image": "images/toyota-camry.jpg",
                    "category": "Sedan",
                    "description": "A reliable and comfortable mid-size sedan. Great for business trips or family travel."
                },
                {
                    "car_id": "CAR-002",
                    "make": "Honda",
                    "model": "CR-V",
                    "year": 2024,
                    "mileage": 8200.0,
                    "available_now": True,
                    "min_rent_period": 1,
                    "max_rent_period": 30,
                    "daily_rate": 95.0,
                    "image": "images/honda-crv.jpg",
                    "category": "SUV",
                    "description": "Spacious SUV with all-wheel drive. Ideal for families and weekend adventures."
                },
                {
                    "car_id": "CAR-003",
                    "make": "BMW",
                    "model": "3 Series",
                    "year": 2023,
                    "mileage": 15000.0,
                    "available_now": True,
                    "min_rent_period": 2,
                    "max_rent_period": 14,
                    "daily_rate": 150.0,
                    "image": "images/bmw-3series.jpg",
                    "category": "Luxury",
                    "description": "Premium German engineering with sporty handling and a luxurious interior."
                },
                {
                    "car_id": "CAR-004",
                    "make": "Hyundai",
                    "model": "i30",
                    "year": 2022,
                    "mileage": 22000.0,
                    "available_now": True,
                    "min_rent_period": 1,
                    "max_rent_period": 30,
                    "daily_rate": 55.0,
                    "image": "images/hyundai-i30.jpg",
                    "category": "Economy",
                    "description": "Fuel-efficient compact hatchback. Perfect for city driving and short trips."
                },
                {
                    "car_id": "CAR-005",
                    "make": "Ford",
                    "model": "Ranger",
                    "year": 2024,
                    "mileage": 5100.0,
                    "available_now": True,
                    "min_rent_period": 2,
                    "max_rent_period": 21,
                    "daily_rate": 110.0,
                    "image": "images/ford-ranger.jpg",
                    "category": "Truck",
                    "description": "4WD dual-cab pickup truck. Great for off-road adventures or moving loads."
                },
                {
                    "car_id": "CAR-006",
                    "make": "Volkswagen",
                    "model": "Golf",
                    "year": 2023,
                    "mileage": 18000.0,
                    "available_now": True,
                    "min_rent_period": 1,
                    "max_rent_period": 30,
                    "daily_rate": 68.0,
                    "image": "images/vw-golf.jpg",
                    "category": "Economy",
                    "description": "A classic European hatchback. Fun to drive with excellent fuel economy."
                },
                {
                    "car_id": "CAR-007",
                    "make": "Mercedes-Benz",
                    "model": "E-Class",
                    "year": 2024,
                    "mileage": 3200.0,
                    "available_now": True,
                    "min_rent_period": 2,
                    "max_rent_period": 14,
                    "daily_rate": 200.0,
                    "image": "images/mercedes-eclass.jpg",
                    "category": "Luxury",
                    "description": "Executive luxury sedan with a smooth ride and sophisticated technology."
                },
                {
                    "car_id": "CAR-008",
                    "make": "Toyota",
                    "model": "RAV4",
                    "year": 2023,
                    "mileage": 11000.0,
                    "available_now": True,
                    "min_rent_period": 1,
                    "max_rent_period": 30,
                    "daily_rate": 88.0,
                    "image": "images/toyota-rav4.jpg",
                    "category": "SUV",
                    "description": "One of the most popular SUVs. Reliable, spacious, and fuel-efficient."
                }
            ]

            for car_data in cars:
                car = Car(**car_data)
                db.session.add(car)

            print("Sample car fleet created (8 vehicles).")
        else:
            print("Cars already exist, skipping.")

        db.session.commit()
        print("\nSeed data complete.")
        print("\nLogin credentials:")
        print("  Admin:    admin@smriticars.com / admin123")
        print("  Customer: james@example.com / customer123")
        print("  Customer: aiko@example.com / customer123")


if __name__ == "__main__":
    seed_database()
