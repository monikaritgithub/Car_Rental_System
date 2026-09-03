"""
Models package — imports all models so SQLAlchemy can discover them.

When db.create_all() is called, SQLAlchemy needs to know about every
model class. Importing them all here makes it easy to do that from
one place: just import this package.
"""

from .additional_charge import AdditionalCharge
from .admin import Admin
from .booking import Booking
from .car import Car
from .customer import Customer
from .payment import Payment

__all__ = ["Customer", "Admin", "Car", "Booking", "Payment", "AdditionalCharge"]
