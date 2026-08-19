"""
Admin model — represents an employee who manages the car rental system.

This maps to the Admin class in the class diagram:
  - employeeId, department, name, email, password
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db


class Admin(db.Model):
    """
    An employee who administers the system.

    Admins can add/update/delete cars, view bookings, approve or cancel
    reservations, confirm payments, and generate reports.
    """

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, plain_password: str) -> None:
        """Hash and store the admin's password securely."""
        self.password_hash = generate_password_hash(plain_password)

    def check_password(self, plain_password: str) -> bool:
        """Return True if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, plain_password)

    def __repr__(self) -> str:
        return f"<Admin {self.name} (ID: {self.employee_id})>"
