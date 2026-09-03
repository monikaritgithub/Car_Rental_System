"""
Booking Engine — the central business logic for creating and managing bookings.

This service implements the sequence diagram workflow exactly:
  - Validate availability and rent period (steps 6-7)
  - Calculate fee using Days × Rate formula (steps 8-9), plus any additional charges
  - Create booking with PENDING status (step 14)
  - Approve or reject bookings (step 19)
  - Update car availability when approved (step 21)

Keeping this logic in a service rather than in route handlers means the
rules stay in one place and can be tested independently of HTTP.
"""

from datetime import date, datetime
from typing import Optional

from database import db
from app.models.booking import Booking, STATUS_PENDING, STATUS_APPROVED, STATUS_REJECTED, STATUS_CANCELLED
from app.models.car import Car
from app.models.payment import Payment, PAYMENT_COMPLETED, PAYMENT_REFUNDED


def _generate_booking_id() -> str:
    """
    Generate the next sequential booking ID, e.g. BKG-0042.

    We look at what's already in the database rather than relying on an
    auto-increment field so the ID stays in a predictable format.
    """
    count = db.session.query(Booking).count()
    return f"BKG-{count + 1:04d}"


def _generate_payment_id() -> str:
    """Generate the next sequential payment ID, e.g. PAY-0042."""
    count = db.session.query(Payment).count()
    return f"PAY-{count + 1:04d}"


def validate_availability(car: Car, start_date: date, end_date: date) -> tuple[bool, str]:
    """
    Check that this car can be booked for these dates.

    This corresponds to sequence diagram step 6:
    'UI → Engine: Validate availability and rent period'

    We check:
    1. The car flag — is it marked available right now?
    2. The date logic — does end come after start?
    3. The rental period — does the number of days fit this car's limits?
    4. No conflicting approved bookings — a car can't be in two places at once

    Returns (True, "") when valid, or (False, reason) when not.
    """
    if not car.available_now:
        return False, "This car is not currently available for booking."

    if start_date < date.today():
        return False, "The start date cannot be in the past."

    if end_date <= start_date:
        return False, "The end date must be after the start date."

    rental_days = (end_date - start_date).days

    if rental_days < car.min_rent_period:
        return False, f"This car requires a minimum rental of {car.min_rent_period} day(s)."

    if rental_days > car.max_rent_period:
        return False, f"This car allows a maximum rental of {car.max_rent_period} day(s)."

    # Check for any overlapping approved bookings for this car.
    # A car might be marked available but have a future approved booking
    # that would conflict.
    overlapping = db.session.query(Booking).filter(
        Booking.car_id == car.id,
        Booking.booking_status == STATUS_APPROVED,
        Booking.start_date < end_date,
        Booking.end_date > start_date
    ).first()

    if overlapping:
        return False, "This car already has an approved booking overlapping your selected dates."

    return True, ""


def calculate_total_fee(daily_rate: float, start_date: date, end_date: date,
                        car: Optional[Car] = None) -> tuple[float, list]:
    """
    Calculate the full rental cost including any additional charges on the car.

    Formula (sequence diagram step 8):
      Base fee = Days × Daily Rate
      Additional charges = sum of per_day charges × days + one_time charges
      Total = Base fee + Additional charges

    Returns a tuple of:
      - total_fee (float): the grand total
      - breakdown (list of dicts): itemised line items for display
    """
    days = (end_date - start_date).days
    base_fee = round(daily_rate * days, 2)

    breakdown = [
        {
            "name": "Base Rental",
            "amount": base_fee,
            "detail": f"${daily_rate:.2f}/day × {days} days"
        }
    ]

    additional_total = 0.0
    if car and car.additional_charges:
        for charge in car.additional_charges:
            charge_amount = charge.calculate_for_days(days)
            additional_total += charge_amount
            detail = (f"${charge.amount:.2f}/day × {days} days"
                      if charge.charge_type == "per_day"
                      else f"${charge.amount:.2f} flat fee")
            breakdown.append({
                "name": charge.name,
                "amount": charge_amount,
                "detail": detail,
                "mandatory": charge.is_mandatory
            })

    total_fee = round(base_fee + additional_total, 2)
    return total_fee, breakdown


def create_booking(customer_id: int, car_id: int, start_date: date,
                   end_date: date, card_number: str, card_holder: str) -> tuple[Optional[Booking], str]:
    """
    Execute the full booking creation workflow from the sequence diagram.

    Steps 14–17 of the sequence diagram:
    - Create booking record with PENDING status (step 14)
    - Save booking to database (step 15)
    - Create associated payment record
    - Return the booking so the UI can show 'booking pending notice' (step 17)

    Returns (booking, "") on success, or (None, error_message) on failure.
    """
    car = db.session.get(Car, car_id)
    if car is None:
        return None, "Car not found."

    # Validate one more time right before creating the booking.
    # The customer might have left the date form open while another booking came in.
    valid, error = validate_availability(car, start_date, end_date)
    if not valid:
        return None, error

    total_fee, _ = calculate_total_fee(car.daily_rate, start_date, end_date, car)

    # Create the booking record
    booking = Booking(
        booking_id=_generate_booking_id(),
        customer_id=customer_id,
        car_id=car_id,
        start_date=start_date,
        end_date=end_date,
        total_fee=total_fee,
        booking_status=STATUS_PENDING
    )
    db.session.add(booking)
    db.session.flush()  # Flush so booking.id is available for the payment FK

    # Create the mock payment record immediately
    payment = Payment(
        payment_id=_generate_payment_id(),
        booking_id=booking.id,
        amount=total_fee
    )
    # Simulate processing the credit card (always succeeds in demo mode)
    payment.process_credit_card(card_number, card_holder)

    db.session.add(payment)
    db.session.commit()

    return booking, ""


def approve_booking(booking_id: str, admin_notes: str = "") -> tuple[bool, str]:
    """
    Admin approves a pending booking.

    Sequence diagram steps 19–21:
    - Update status to APPROVED (step 20)
    - Set car availableNow = false (step 21)

    Returns (True, "") on success, or (False, reason) on failure.
    """
    booking = db.session.query(Booking).filter_by(booking_id=booking_id).first()
    if booking is None:
        return False, "Booking not found."

    if booking.booking_status != STATUS_PENDING:
        return False, f"Only PENDING bookings can be approved. Current status: {booking.booking_status}"

    # Update the booking status
    booking.booking_status = STATUS_APPROVED
    booking.admin_notes = admin_notes
    booking.updated_at = datetime.utcnow()

    # Mark the car as no longer available — exactly as shown in step 21:
    # 'Engine → DB: Update car availableNow = false'
    car = db.session.get(Car, booking.car_id)
    if car:
        car.set_availability(False)

    db.session.commit()
    return True, ""


def reject_booking(booking_id: str, admin_notes: str = "") -> tuple[bool, str]:
    """
    Admin rejects a pending booking.

    The car remains available since the booking never went through.
    The payment is marked REFUNDED since the customer already paid.
    """
    booking = db.session.query(Booking).filter_by(booking_id=booking_id).first()
    if booking is None:
        return False, "Booking not found."

    if booking.booking_status != STATUS_PENDING:
        return False, f"Only PENDING bookings can be rejected. Current status: {booking.booking_status}"

    booking.booking_status = STATUS_REJECTED
    booking.admin_notes = admin_notes
    booking.updated_at = datetime.utcnow()

    # Mark the payment as refunded — the customer paid but the booking was rejected
    if booking.payment and booking.payment.payment_status == PAYMENT_COMPLETED:
        booking.payment.payment_status = PAYMENT_REFUNDED
        booking.payment.confirmed_at = datetime.utcnow()

    # The car stays available since the booking was rejected
    db.session.commit()
    return True, ""


def admin_cancel_approved_booking(booking_id: str, admin_notes: str = "") -> tuple[bool, str]:
    """
    Admin cancels an already-APPROVED booking and issues a refund.

    This handles the case where:
      1. Customer paid → payment was COMPLETED
      2. Admin approved the booking → car marked unavailable
      3. Admin later needs to cancel (e.g., car breaks down, double booking)

    On cancellation:
      - Booking status → CANCELLED
      - Car → available again (set available_now = True)
      - Payment → REFUNDED

    Returns (True, "") on success or (False, reason) on failure.
    """
    booking = db.session.query(Booking).filter_by(booking_id=booking_id).first()
    if booking is None:
        return False, "Booking not found."

    if booking.booking_status != STATUS_APPROVED:
        return False, f"Only APPROVED bookings can be cancelled via this action. Current status: {booking.booking_status}"

    # Cancel the booking
    booking.booking_status = STATUS_CANCELLED
    booking.admin_notes = (booking.admin_notes or "") + f"\n[CANCELLED] {admin_notes}".strip()
    booking.updated_at = datetime.utcnow()

    # Set car back to available — the rental is no longer happening
    car = db.session.get(Car, booking.car_id)
    if car:
        car.set_availability(True)

    # Issue the refund on the payment record
    if booking.payment:
        booking.payment.payment_status = PAYMENT_REFUNDED
        booking.payment.confirmed_at = datetime.utcnow()

    db.session.commit()
    return True, ""


def cancel_booking_by_customer(booking_id: str, customer_id: int) -> tuple[bool, str]:
    """
    Customer cancels their own reservation.

    This is the 'Cancel Reservation' use case from the use case diagram.
    Customers can only cancel bookings that are still PENDING.
    Once approved, they would need to contact the rental company.
    """
    booking = db.session.query(Booking).filter_by(
        booking_id=booking_id,
        customer_id=customer_id
    ).first()

    if booking is None:
        return False, "Booking not found or does not belong to your account."

    if booking.booking_status not in (STATUS_PENDING,):
        return False, "Only pending bookings can be cancelled. Please contact us for approved bookings."

    booking.booking_status = STATUS_CANCELLED
    booking.updated_at = datetime.utcnow()

    # Refund the payment since it was already completed
    if booking.payment and booking.payment.payment_status == PAYMENT_COMPLETED:
        booking.payment.payment_status = PAYMENT_REFUNDED

    db.session.commit()
    return True, ""
