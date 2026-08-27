import os
import pytest
from app.customer_app import create_customer_app
from app.admin_app import create_admin_app
from database import db
from config.settings import TestingConfig
from app.models import Customer, Admin, Car

@pytest.fixture
def customer_app():
    """Create a customer Flask app configured for testing."""
    app = create_customer_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def customer_client(customer_app):
    return customer_app.test_client()

@pytest.fixture
def admin_app():
    """Create an admin Flask app configured for testing."""
    app = create_admin_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def admin_client(admin_app):
    return admin_app.test_client()

@pytest.fixture
def sample_customer(customer_app):
    """Create and return a sample customer."""
    with customer_app.app_context():
        customer = Customer(
            name="Test User",
            email="test@example.com",
            phone_no="123456789",
            license_id_no="LIC-123"
        )
        customer.set_password("password123")
        db.session.add(customer)
        db.session.commit()
        return customer

@pytest.fixture
def sample_admin(admin_app):
    """Create and return a sample admin."""
    with admin_app.app_context():
        admin = Admin(
            employee_id="EMP-999",
            name="Test Admin",
            email="admin@example.com"
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        return admin

@pytest.fixture
def sample_car(customer_app):
    """Create and return a sample car."""
    with customer_app.app_context():
        car = Car(
            car_id="CAR-TEST",
            make="TestMake",
            model="TestModel",
            year=2024,
            daily_rate=50.0,
            available_now=True
        )
        db.session.add(car)
        db.session.commit()
        return car
