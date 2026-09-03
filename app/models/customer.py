"""
Customer model — represents a registered customer in the system.

This maps directly to the Customer class defined in the class diagram:
  - licenseIDNo, paymentInfo, name, email, password, phoneNo, address

Passwords are stored as Werkzeug hashes, never as plain text.
"""

from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from database import db


class Customer(db.Model):
    """
    A person who registers, browses cars, makes bookings, and payments.

    The license ID is important for a car rental business — it is used to
    verify the driver before handing over the keys.
    """

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    license_id_no = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(300), nullable=True)

    # payment_info stores the last 4 digits of the card or a billing reference,
    # not a full card number — we never store raw card data
    payment_info = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One customer can have many bookings
    bookings = db.relationship("Booking", backref="customer", lazy=True)

    def __init__(self, *, name: str, email: str, phone_no: str,
                 license_id_no: str, address: str = "",
                 payment_info: str = "") -> None:
        self.name = name
        self.email = email
        self.phone_no = phone_no
        self.license_id_no = license_id_no
        self.address = address
        self.payment_info = payment_info

    def set_password(self, plain_password: str) -> None:
        """
        Hash and store the customer's password.

        Werkzeug's generate_password_hash uses PBKDF2-SHA256 by default,
        which is a well-regarded approach for web applications.
        """
        self.password_hash = generate_password_hash(plain_password)

    def check_password(self, plain_password: str) -> bool:
        """Return True if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, plain_password)

    def __repr__(self) -> str:
        return f"<Customer {self.name} ({self.email})>"
