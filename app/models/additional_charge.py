"""
AdditionalCharge model — optional or mandatory extra fees that can be
attached to a specific car.

Examples: GPS Navigation, Child Seat, Additional Driver, Airport Surcharge,
         Full Insurance Coverage, Young Driver Fee, etc.

These charges are shown to the customer during booking so the total fee
is transparent before payment is made.

Design:
  - charge_type = 'per_day'  → amount × number of rental days
  - charge_type = 'one_time' → flat amount regardless of duration
  - is_mandatory = True      → always added to booking; customer cannot opt out
  - is_mandatory = False     → optional; customer can choose to add it
"""

from datetime import datetime
from database import db


CHARGE_TYPE_PER_DAY = "per_day"
CHARGE_TYPE_ONE_TIME = "one_time"
VALID_CHARGE_TYPES = {CHARGE_TYPE_PER_DAY, CHARGE_TYPE_ONE_TIME}


class AdditionalCharge(db.Model):
    """
    An extra fee that can be linked to one specific car in the fleet.

    Admins define these charges per car (e.g. the Luxury BMW might have
    a mandatory full-coverage insurance charge of $25/day). The booking
    engine reads all charges for the booked car and adds them to the total.
    """

    __tablename__ = "additional_charges"

    id = db.Column(db.Integer, primary_key=True)

    # The car this charge belongs to
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)

    # Human-readable name shown to customers, e.g. "GPS Navigation"
    name = db.Column(db.String(100), nullable=False)

    # The dollar amount for this charge
    amount = db.Column(db.Float, nullable=False)

    # Whether this is a flat one-time fee or a daily recurring charge
    charge_type = db.Column(db.String(20), default=CHARGE_TYPE_ONE_TIME, nullable=False)

    # Mandatory charges are always included; optional ones the customer sees
    # but in the current implementation they are all included for simplicity.
    # A future version could let customers opt out of non-mandatory charges.
    is_mandatory = db.Column(db.Boolean, default=True, nullable=False)

    # Optional description shown in the booking breakdown
    description = db.Column(db.String(200), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def calculate_for_days(self, rental_days: int) -> float:
        """
        Return the total cost of this charge given a rental duration.

        per_day charges scale with duration; one_time charges are flat.
        """
        if self.charge_type == CHARGE_TYPE_PER_DAY:
            return round(self.amount * rental_days, 2)
        return round(self.amount, 2)

    def __repr__(self) -> str:
        rate = f"${self.amount}/day" if self.charge_type == CHARGE_TYPE_PER_DAY else f"${self.amount} one-time"
        mandatory = "mandatory" if self.is_mandatory else "optional"
        return f"<AdditionalCharge '{self.name}' {rate} ({mandatory})>"
