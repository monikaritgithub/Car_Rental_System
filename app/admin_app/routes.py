"""
Admin routes — all pages and actions for the admin interface.

These routes implement the Admin use cases from the use case diagram:
  - Login
  - Add Car
  - Update Car
  - Delete Car
  - View Reservation/Booking
  - Confirm/Cancel Booking
  - Confirm Payment
  - Generate Report

The admin session is separate from the customer session because
these are two different Flask applications running on different ports.
"""

import os
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, send_from_directory
)

from database import db
from app.models.admin import Admin
from app.models.booking import Booking, STATUS_PENDING, STATUS_APPROVED
from app.models.payment import Payment
from app.models.customer import Customer
from app.models.car import Car
from app.models.additional_charge import AdditionalCharge, VALID_CHARGE_TYPES
from app.services import car_service, booking_engine, payment_service, report_service
from config.settings import BASE_DIR
from functools import wraps

# Allowed image extensions for car photo uploads
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}


def _allowed_file(filename: str) -> bool:
    """Return True if the filename has an allowed image extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _save_car_image(file_storage) -> str:
    """
    Save an uploaded car image to the project images/ directory.

    Returns the filename (e.g. 'my-car.jpg') which is stored in the DB.
    The serve_image route then serves it from the images/ folder.
    """
    filename = secure_filename(file_storage.filename)
    images_dir = str(BASE_DIR / 'images')
    os.makedirs(images_dir, exist_ok=True)
    save_path = os.path.join(images_dir, filename)
    file_storage.save(save_path)
    return filename

admin_bp = Blueprint("admin", __name__)


# ─── Helper ────────────────────────────────────────────────────────────────────

def admin_required(f):
    """Redirect to admin login if no admin session is active."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin_id" not in session:
            flash("Admin login required.", "warning")
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


# ─── Static image serving ──────────────────────────────────────────────────────

@admin_bp.route("/images/<path:filename>")
def serve_image(filename):
    """Serve car images from the shared project-level images/ directory."""
    images_dir = str(BASE_DIR / "images")
    return send_from_directory(images_dir, filename)


# ─── Authentication ────────────────────────────────────────────────────────────

@admin_bp.route("/")
def root():
    """Redirect root to dashboard or login."""
    if "admin_id" in session:
        return redirect(url_for("admin.dashboard"))
    return redirect(url_for("admin.login"))


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    """Admin login — separate from the customer login."""
    if "admin_id" in session:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        admin = db.session.query(Admin).filter_by(email=email.lower()).first()
        if admin and admin.check_password(password):
            session["admin_id"] = admin.id
            session["admin_name"] = admin.name
            session["admin_employee_id"] = admin.employee_id
            flash(f"Welcome, {admin.name}!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Incorrect credentials. Please try again.", "error")

    return render_template("login.html")


@admin_bp.route("/logout")
def logout():
    """Clear admin session."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin.login"))


# ─── Dashboard ─────────────────────────────────────────────────────────────────

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """
    Admin dashboard — overview of the system state.

    Shows counts of pending bookings, total cars, customers, and
    quick access to the main management sections.
    """
    pending_count = db.session.query(Booking).filter_by(booking_status=STATUS_PENDING).count()
    total_cars = db.session.query(Car).count()
    available_cars = db.session.query(Car).filter_by(available_now=True).count()
    total_customers = db.session.query(Customer).count()
    total_bookings = db.session.query(Booking).count()

    recent_bookings = (
        db.session.query(Booking)
        .order_by(Booking.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template("dashboard.html",
                           pending_count=pending_count,
                           total_cars=total_cars,
                           available_cars=available_cars,
                           total_customers=total_customers,
                           total_bookings=total_bookings,
                           recent_bookings=recent_bookings)


# ─── Car Management ────────────────────────────────────────────────────────────

@admin_bp.route("/cars")
@admin_required
def cars():
    """List all cars in the fleet — admin sees all, not just available ones."""
    all_cars = car_service.get_all_cars()
    return render_template("cars.html", cars=all_cars)


@admin_bp.route("/cars/add", methods=["GET", "POST"])
@admin_required
def add_car():
    """
    Add a new car to the fleet.
    """
    if request.method == "POST":
        try:
            make = request.form.get("make", "").strip()
            model = request.form.get("model", "").strip()
            year = int(request.form.get("year", 0))
            mileage = float(request.form.get("mileage", 0))
            daily_rate = float(request.form.get("daily_rate", 0))
            min_rent = int(request.form.get("min_rent_period", 1))
            max_rent = int(request.form.get("max_rent_period", 30))
            description = request.form.get("description", "").strip()
            category = request.form.get("category", "").strip()
        except ValueError:
            flash("Please enter valid numbers for year, mileage, and daily rate.", "error")
            return render_template("car_form.html", car=None, action="add")

        if not all([make, model, year, daily_rate]):
            flash("Make, model, year, and daily rate are required.", "error")
            return render_template("car_form.html", car=None, action="add")

        # Handle optional car photo upload
        image_filename = ""
        uploaded_file = request.files.get("car_image")
        if uploaded_file and uploaded_file.filename:
            if not _allowed_file(uploaded_file.filename):
                flash("Invalid image type. Use JPG, PNG, WEBP, or GIF.", "error")
                return render_template("car_form.html", car=None, action="add")
            image_filename = _save_car_image(uploaded_file)

        car = car_service.add_car(
            make=make, model=model, year=year, mileage=mileage,
            daily_rate=daily_rate, min_rent=min_rent, max_rent=max_rent,
            image=image_filename, description=description, category=category
        )
        flash(f"Car {car.car_id} ({car.year} {car.make} {car.model}) added successfully.", "success")
        return redirect(url_for("admin.cars"))

    return render_template("car_form.html", car=None, action="add")


@admin_bp.route("/cars/edit/<car_id>", methods=["GET", "POST"])
@admin_required
def edit_car(car_id):
    """
    Edit a car's details.
    """
    car = car_service.get_car_by_id(car_id)
    if car is None:
        flash("Car not found.", "error")
        return redirect(url_for("admin.cars"))

    if request.method == "POST":
        try:
            updates = {
                "make": request.form.get("make", "").strip(),
                "model": request.form.get("model", "").strip(),
                "year": int(request.form.get("year", car.year)),
                "mileage": float(request.form.get("mileage", car.mileage)),
                "daily_rate": float(request.form.get("daily_rate", car.daily_rate)),
                "min_rent_period": int(request.form.get("min_rent_period", car.min_rent_period)),
                "max_rent_period": int(request.form.get("max_rent_period", car.max_rent_period)),
                "description": request.form.get("description", "").strip(),
                "category": request.form.get("category", "").strip(),
            }
        except ValueError:
            flash("Please enter valid numbers for year, mileage, and daily rate.", "error")
            return render_template("car_form.html", car=car, action="edit")

        # Handle optional new photo upload — keep existing if no new file provided
        uploaded_file = request.files.get("car_image")
        if uploaded_file and uploaded_file.filename:
            if not _allowed_file(uploaded_file.filename):
                flash("Invalid image type. Use JPG, PNG, WEBP, or GIF.", "error")
                return render_template("car_form.html", car=car, action="edit")
            updates["image"] = _save_car_image(uploaded_file)
        # If no new file, do NOT update the image field (keep existing)

        success, error = car_service.update_car(car_id, **updates)
        if success:
            flash(f"Car {car_id} updated successfully.", "success")
            return redirect(url_for("admin.cars"))
        else:
            flash(error, "error")

    return render_template("car_form.html", car=car, action="edit")


@admin_bp.route("/cars/delete/<car_id>", methods=["POST"])
@admin_required
def delete_car(car_id):
    """
    Delete a car from the fleet.
    Cars with active bookings cannot be deleted.
    """
    success, error = car_service.delete_car(car_id)
    if success:
        flash(f"Car {car_id} has been removed from the fleet.", "success")
    else:
        flash(error, "error")
    return redirect(url_for("admin.cars"))


# ─── Booking Management ────────────────────────────────────────────────────────

@admin_bp.route("/bookings")
@admin_required
def bookings():
    """
    View all reservations.
    Filter by status if a query parameter is provided.
    """
    status_filter = request.args.get("status", "")
    query = db.session.query(Booking).order_by(Booking.created_at.desc())

    if status_filter:
        query = query.filter_by(booking_status=status_filter.upper())

    all_bookings = query.all()
    return render_template("bookings.html", bookings=all_bookings, status_filter=status_filter)


@admin_bp.route("/bookings/<booking_id>")
@admin_required
def booking_detail(booking_id):
    """Detailed view of a single booking including customer and car info."""
    booking = db.session.query(Booking).filter_by(booking_id=booking_id).first()
    if booking is None:
        flash("Booking not found.", "error")
        return redirect(url_for("admin.bookings"))
    return render_template("booking_detail.html", booking=booking)


@admin_bp.route("/bookings/approve/<booking_id>", methods=["POST"])
@admin_required
def approve_booking(booking_id):
    """
    Approve a pending booking and mark the car as unavailable.
    """
    notes = request.form.get("admin_notes", "").strip()
    success, error = booking_engine.approve_booking(booking_id, admin_notes=notes)

    if success:
        flash(f"Booking {booking_id} has been approved. The car has been marked unavailable.", "success")
    else:
        flash(error, "error")

    return redirect(url_for("admin.bookings"))


@admin_bp.route("/bookings/reject/<booking_id>", methods=["POST"])
@admin_required
def reject_booking(booking_id):
    """
    Reject a pending booking.
    The payment is automatically marked as REFUNDED since the customer
    already paid and the booking will not proceed.
    """
    notes = request.form.get("admin_notes", "").strip()
    success, error = booking_engine.reject_booking(booking_id, admin_notes=notes)

    if success:
        flash(f"Booking {booking_id} has been rejected and payment marked for refund.", "success")
    else:
        flash(error, "error")

    return redirect(url_for("admin.bookings"))


@admin_bp.route("/bookings/cancel-refund/<booking_id>", methods=["POST"])
@admin_required
def cancel_and_refund_booking(booking_id):
    """
    Cancel an already-APPROVED booking and issue a refund.

    The booking status changes to CANCELLED, the car becomes available again,
    and the payment is marked REFUNDED.
    """
    notes = request.form.get("admin_notes", "").strip()
    success, error = booking_engine.admin_cancel_approved_booking(
        booking_id, admin_notes=notes
    )

    if success:
        flash(
            f"Booking {booking_id} has been cancelled and payment refunded. "
            f"The car is now available again.",
            "success"
        )
    else:
        flash(error, "error")

    return redirect(url_for("admin.booking_detail", booking_id=booking_id))


# ─── Payment Management ────────────────────────────────────────────────────────

@admin_bp.route("/payments")
@admin_required
def payments():
    """View all payment records."""
    all_payments = payment_service.get_all_payments()
    return render_template("payments.html", payments=all_payments)


@admin_bp.route("/payments/confirm/<payment_id>", methods=["POST"])
@admin_required
def confirm_payment(payment_id):
    """
    Admin confirms a payment manually.
    """
    success, error = payment_service.admin_confirm_payment(payment_id)
    if success:
        flash(f"Payment {payment_id} has been confirmed.", "success")
    else:
        flash(error, "error")
    return redirect(url_for("admin.payments"))


# ─── Additional Charges Management ────────────────────────────────────────────

@admin_bp.route("/cars/<car_id>/charges/add", methods=["POST"])
@admin_required
def add_charge(car_id):
    """
    Add an additional charge to a car.

    Admins define extra fees (GPS, insurance, airport fee, etc.)
    on a per-car basis. These are included in the booking fee calculation.
    """
    car = car_service.get_car_by_id(car_id)
    if car is None:
        flash("Car not found.", "error")
        return redirect(url_for("admin.cars"))

    try:
        name = request.form.get("charge_name", "").strip()
        amount = float(request.form.get("charge_amount", 0))
        charge_type = request.form.get("charge_type", "one_time")
        is_mandatory = request.form.get("is_mandatory", "true") == "true"
        description = request.form.get("charge_description", "").strip()
    except ValueError:
        flash("Invalid charge amount.", "error")
        return redirect(url_for("admin.edit_car", car_id=car_id))

    if not name or amount <= 0:
        flash("Charge name and a positive amount are required.", "error")
        return redirect(url_for("admin.edit_car", car_id=car_id))

    if charge_type not in VALID_CHARGE_TYPES:
        flash("Invalid charge type.", "error")
        return redirect(url_for("admin.edit_car", car_id=car_id))

    charge = AdditionalCharge(
        car_id=car.id,
        name=name,
        amount=amount,
        charge_type=charge_type,
        is_mandatory=is_mandatory,
        description=description
    )
    db.session.add(charge)
    db.session.commit()

    flash(f"Charge '{name}' added to {car.car_id} successfully.", "success")
    return redirect(url_for("admin.edit_car", car_id=car_id))


@admin_bp.route("/cars/<car_id>/charges/delete/<int:charge_id>", methods=["POST"])
@admin_required
def delete_charge(car_id, charge_id):
    """Delete an additional charge from a car."""
    charge = db.session.get(AdditionalCharge, charge_id)
    if charge is None:
        flash("Charge not found.", "error")
    else:
        charge_name = charge.name
        db.session.delete(charge)
        db.session.commit()
        flash(f"Charge '{charge_name}' removed.", "success")

    return redirect(url_for("admin.edit_car", car_id=car_id))


# ─── Report ────────────────────────────────────────────────────────────────────

@admin_bp.route("/report")
@admin_required
def report():
    """
    Generate a system-wide summary report for the dashboard.
    """
    data = report_service.generate_summary_report()
    return render_template("report.html", data=data)

