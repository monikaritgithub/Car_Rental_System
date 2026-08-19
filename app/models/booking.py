"""
Booking model — represents a reservation made by a customer for a car.

This maps to the Booking class in the class diagram:
  - bookingId, customerId, carId, startDate, endDate,
    totalFee, bookingStatus

The sequence diagram defines these status values:
  PENDING    — booking created after payment, awaiting admin action
  APPROVED   — admin confirmed the booking, car set to unavailable
  REJECTED   — admin declined the booking
  CANCELLED  — customer cancelled before admin reviewed
"""

from datetime import datetime, date
from database import db


# Status constants — using strings as shown in the class diagram,
# but defined here so we avoid typos in multiple places
STATUS_PENDING = "PENDING"
STATUS_APPROVED = "APPROVED"
STATUS_REJECTED = "REJECTED"
STATUS_CANCELLED = "CANCELLED"

VALID_STATUSES = {STATUS_PENDING, STATUS_APPROVED, STATUS_REJECTED, STATUS_CANCELLED}


class Booking(db.Model):
    """
    A reservation linking a Customer to a Car for a date range.

    The workflow follows the sequence diagram exactly:
    1. Customer selects dates, fee is calculated
    2. Customer pays (mock payment)
    3. Booking is created with status PENDING
    4. Admin sees the pending booking and approves or rejects it
    5. On approval, the car is marked unavailable
    6. Customer receives final confirmation
    """

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    # Human-readable booking reference, e.g. "BKG-0001"
    booking_id = db.Column(db.String(20), unique=True, nullable=False)

    # Foreign keys linking to customer and car tables
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_fee = db.Column(db.Float, nullable=False)

    # Status follows the sequence diagram: PENDING → APPROVED or REJECTED
    booking_status = db.Column(db.String(20), default=STATUS_PENDING, nullable=False)

    # Additional notes admin can add when approving or rejecting
    admin_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # One booking requires exactly one payment record
    payment = db.relationship("Payment", backref="booking", uselist=False, lazy=True)

    def calculate_total_fee(self, daily_rate: float, days: int) -> float:
        """
        Calculate the rental fee: total = days × daily_rate

        This is exactly the formula shown in the sequence diagram step 8:
        'Request fee calculation (Days × Rate)'
        """
        return round(daily_rate * days, 2)

    def validate_availability(self, car_available: bool, start_date: date,
                              end_date: date, min_days: int, max_days: int) -> tuple[bool, str]:
        """
        Check that the booking dates make sense and the car is free.

        Returns a tuple of (is_valid, error_message).
        The error message is empty when valid.
        """
        if not car_available:
            return False, "This car is not currently available."

        if end_date <= start_date:
            return False, "End date must be after start date."

        if start_date < date.today():
            return False, "Start date cannot be in the past."

        rental_days = (end_date - start_date).days
        if rental_days < min_days:
            return False, f"Minimum rental period for this car is {min_days} day(s)."
        if rental_days > max_days:
            return False, f"Maximum rental period for this car is {max_days} day(s)."

        return True, ""

    def update_status(self, new_status: str) -> bool:
        """
        Change the booking status.

        Only transitions to known status values are allowed.
        Returns True if the update was accepted.
        """
        if new_status not in VALID_STATUSES:
            return False
        self.booking_status = new_status
        self.updated_at = datetime.utcnow()
        return True

    @property
    def rental_days(self) -> int:
        """How many days the rental covers."""
        return (self.end_date - self.start_date).days

    def __repr__(self) -> str:
        return f"<Booking {self.booking_id}: {self.booking_status}>"
