"""
Customer service — handles customer registration and authentication.

This implements:
  - Login/Register from the customer use case diagram
  - Profile data for the customer class diagram
"""

from typing import Optional
from database import db
from app.models.customer import Customer


def register_customer(name: str, email: str, password: str,
                       phone_no: str, license_id_no: str,
                       address: str = "") -> tuple[Optional[Customer], str]:
    """
    Register a new customer account.

    Checks for duplicate email and license ID before creating the account.
    Returns (customer, "") on success, or (None, error) on failure.
    """
    # An email can only belong to one account
    if db.session.query(Customer).filter_by(email=email.lower().strip()).first():
        return None, "An account with this email address already exists."

    # License IDs are unique identifiers — two accounts can't share one
    if db.session.query(Customer).filter_by(license_id_no=license_id_no.strip()).first():
        return None, "This license ID is already registered to another account."

    customer = Customer(
        name=name.strip(),
        email=email.lower().strip(),
        phone_no=phone_no.strip(),
        license_id_no=license_id_no.strip(),
        address=address.strip()
    )
    customer.set_password(password)

    db.session.add(customer)
    db.session.commit()
    return customer, ""


def authenticate_customer(email: str, password: str) -> Optional[Customer]:
    """
    Verify login credentials and return the Customer if valid.

    Returns None if the email doesn't exist or the password is wrong.
    We deliberately give the same response for both cases — this prevents
    attackers from learning which emails are registered.
    """
    customer = db.session.query(Customer).filter_by(
        email=email.lower().strip()
    ).first()

    if customer and customer.check_password(password):
        return customer
    return None


def get_customer_by_id(customer_id: int) -> Optional[Customer]:
    """Retrieve a customer record by primary key."""
    return db.session.get(Customer, customer_id)
