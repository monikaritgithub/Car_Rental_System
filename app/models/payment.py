"""
Payment model — represents the payment record for a booking.

This maps to the Payment class in the class diagram:
  - paymentId, bookingId, amount, paymentDate, paymentStatus

The sequence diagram shows the payment flow:
  Step 11: Customer enters card details and pays
  Step 12: UI sends transaction to Payment Gateway (mock)
  Step 13: Payment Gateway returns approval
  After admin approval, admin can also 'Confirm Payment' from their interface
"""

from datetime import datetime

from database import db

# Payment status values
PAYMENT_PENDING = "PENDING"
PAYMENT_COMPLETED = "COMPLETED"
PAYMENT_FAILED = "FAILED"
PAYMENT_REFUNDED = "REFUNDED"


class Payment(db.Model):
    """
    A financial record linked to one booking.

    This is a mock implementation — no real money moves.
    The payment record is created when the customer submits the checkout form
    and is marked COMPLETED immediately (simulating instant gateway approval).

    In a real system you would call an actual Stripe or PayPal API here
    and handle webhooks for asynchronous confirmation.
    """

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    # Human-readable reference, e.g. "PAY-0001"
    payment_id = db.Column(db.String(20), unique=True, nullable=False)

    # Each payment belongs to exactly one booking
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)

    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_status = db.Column(db.String(20), default=PAYMENT_PENDING, nullable=False)

    # We store only the last four digits of the card for display purposes.
    # Storing full card numbers would be a serious security violation.
    card_last_four = db.Column(db.String(4), nullable=True)

    # The card holder name entered on the checkout form
    card_holder_name = db.Column(db.String(100), nullable=True)

    # When admin manually confirms a payment from the admin panel
    confirmed_by_admin = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, *, payment_id: str, booking_id: int, amount: float,
                 payment_status: str = PAYMENT_PENDING) -> None:
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.payment_status = payment_status

    def process_credit_card(self, card_number: str, card_holder: str) -> bool:
        """
        Simulate processing a credit card payment.

        In this demo system this always succeeds. We record only the
        last four digits of the card number for display on receipts.
        Returns True to indicate a successful mock transaction.
        """
        # Strip spaces and store only the last 4 digits
        cleaned = card_number.replace(" ", "").replace("-", "")
        self.card_last_four = cleaned[-4:] if len(cleaned) >= 4 else "0000"
        self.card_holder_name = card_holder
        self.payment_status = PAYMENT_COMPLETED
        self.payment_date = datetime.utcnow()
        return True

    def confirm_payment(self) -> None:
        """
        Mark this payment as confirmed by an admin.

        This corresponds to the 'Confirm Payment' use case in the diagram.
        """
        self.confirmed_by_admin = True
        self.confirmed_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Payment {self.payment_id}: ${self.amount:.2f} ({self.payment_status})>"
