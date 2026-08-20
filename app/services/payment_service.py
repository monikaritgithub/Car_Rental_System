"""
Payment service — handles payment operations and admin confirmation.

This implements:
  - Make Payment (Customer use case) — handled in booking_engine, but
    admin confirmation lives here
  - Confirm Payment (Admin use case)
"""

from datetime import datetime
from typing import Optional

from database import db
from app.models.payment import Payment, PAYMENT_COMPLETED


def get_payment_by_booking_id(booking_db_id: int) -> Optional[Payment]:
    """Find the payment record associated with a booking's database ID."""
    return db.session.query(Payment).filter_by(booking_id=booking_db_id).first()


def get_all_payments() -> list[Payment]:
    """Return all payment records, newest first."""
    return db.session.query(Payment).order_by(Payment.payment_date.desc()).all()


def admin_confirm_payment(payment_id: str) -> tuple[bool, str]:
    """
    Admin manually confirms a payment from the admin interface.

    This matches the 'Confirm Payment' use case in the use case diagram
    and the Admin.confirmPayment() method in the class diagram.

    In this demo the payment is already marked COMPLETED by the mock
    gateway, but the admin confirmation adds a second layer of approval
    for record-keeping purposes.
    """
    payment = db.session.query(Payment).filter_by(payment_id=payment_id).first()
    if payment is None:
        return False, "Payment record not found."

    if payment.payment_status != PAYMENT_COMPLETED:
        return False, "Only completed payments can be confirmed."

    payment.confirm_payment()
    db.session.commit()
    return True, ""
