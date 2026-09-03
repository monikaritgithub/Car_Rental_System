"""
Report service — generates summary data for the admin 'Generate Report' use case.

The use case diagram shows 'Generate Report' as an admin-only feature.
This service collects aggregated data from the database so the admin
template can display a meaningful business summary.
"""

from app.models.booking import (STATUS_APPROVED, STATUS_CANCELLED,
                                STATUS_PENDING, STATUS_REJECTED, Booking)
from app.models.car import Car
from app.models.customer import Customer
from app.models.payment import PAYMENT_COMPLETED, Payment
from database import db


def generate_summary_report() -> dict[str, object]:
    """
    Collect key statistics across the entire system.

    Returns a dictionary of numbers and lists that the report template
    uses to render tables and totals.
    """
    # Count totals for the summary cards at the top of the report
    total_cars = db.session.query(Car).count()
    available_cars = db.session.query(Car).filter_by(available_now=True).count()
    total_customers = db.session.query(Customer).count()

    # Booking counts broken down by status
    total_bookings = db.session.query(Booking).count()
    pending_bookings = db.session.query(Booking).filter_by(booking_status=STATUS_PENDING).count()
    approved_bookings = db.session.query(Booking).filter_by(booking_status=STATUS_APPROVED).count()
    rejected_bookings = db.session.query(Booking).filter_by(booking_status=STATUS_REJECTED).count()
    cancelled_bookings = db.session.query(Booking).filter_by(booking_status=STATUS_CANCELLED).count()

    # Revenue is the sum of completed payments
    # We only count payments that actually went through
    completed_payments = db.session.query(Payment).filter_by(
        payment_status=PAYMENT_COMPLETED
    ).all()
    total_revenue = sum(p.amount for p in completed_payments)

    # The 10 most recent bookings with their related data for the detail table
    recent_bookings = (
        db.session.query(Booking)
        .order_by(Booking.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "total_cars": total_cars,
        "available_cars": available_cars,
        "unavailable_cars": total_cars - available_cars,
        "total_customers": total_customers,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "approved_bookings": approved_bookings,
        "rejected_bookings": rejected_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_revenue": round(total_revenue, 2),
        "total_payments": len(completed_payments),
        "recent_bookings": recent_bookings,
    }
