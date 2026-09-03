"""
Models package — imports all models so SQLAlchemy can discover them.

When db.create_all() is called, SQLAlchemy needs to know about every
model class. Importing them all here makes it easy to do that from
one place: just import this package.
"""

from .customer import Customer
from .admin import Admin
from .car import Car
from .booking import Booking
from .payment import Payment
from .additional_charge import AdditionalCharge

__all__ = ["Customer", "Admin", "Car", "Booking", "Payment", "AdditionalCharge"]
