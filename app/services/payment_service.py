"""
Payment service — handles payment operations and admin confirmation/refunds.

This implements:
  - Make Payment (Customer use case) — handled in booking_engine
  - Confirm Payment (Admin use case)
  - Refund Payment (Admin use case) — when approved booking is cancelled
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import desc

from app.models.payment import PAYMENT_COMPLETED, PAYMENT_REFUNDED, Payment
from database import db


def get_payment_by_booking_id(booking_db_id: int) -> Optional[Payment]:
    """Find the payment record associated with a booking's database ID."""
    return db.session.query(Payment).filter_by(booking_id=booking_db_id).first()  # type: ignore[return-value]


def get_all_payments() -> list[Payment]:
    """Return all payment records, newest first."""
    return db.session.query(Payment).order_by(desc(Payment.payment_date)).all()  # type: ignore[return-value]


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


def admin_refund_payment(payment_id: str) -> tuple[bool, str]:
    """
    Admin manually issues a refund for a payment.

    Called when an approved booking is cancelled after payment was
    already collected. Marks the payment status as REFUNDED so the
    customer and admin can see the refund has been processed.

    In a real system this would call the payment gateway's refund API.
    In this demo system, it simply updates the status in the database.
    """
    payment = db.session.query(Payment).filter_by(payment_id=payment_id).first()
    if payment is None:
        return False, "Payment record not found."

    if payment.payment_status == PAYMENT_REFUNDED:
        return False, "This payment has already been refunded."

    if payment.payment_status not in (PAYMENT_COMPLETED,):
        return False, "Only completed payments can be refunded."

    payment.payment_status = PAYMENT_REFUNDED
    payment.confirmed_at = datetime.utcnow()
    db.session.commit()
    return True, ""
