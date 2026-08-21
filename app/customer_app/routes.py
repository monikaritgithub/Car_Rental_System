"""
Customer routes — all pages and actions for the customer-facing interface.

These routes implement the Customer use cases from the use case diagram:
  - Login/Register
  - Search/View Cars (includes View Car Details)
  - Book/Reserve Car (includes Calculate Rental Fee, Validate Availability)
  - Cancel Reservation
  - Make Payment (includes Process Credit Card)

The session is used for lightweight authentication — we store the
customer's ID and name after login.
"""

import os
from datetime import datetime, date
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, send_from_directory, current_app
)

from database import db
from app.models.booking import Booking
from app.services import car_service, customer_service, booking_engine
from config.settings import BASE_DIR

# All customer routes live under this blueprint
customer_bp = Blueprint("customer", __name__)


# ─── Helper ────────────────────────────────────────────────────────────────────

def customer_required(f):
    """
    Decorator that redirects to the login page if no customer is signed in.

    We use a simple session-based approach — when the customer logs in we
    store their ID in the session, and when they log out we clear it.
    """
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "customer_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("customer.login"))
        return f(*args, **kwargs)
    return decorated


# ─── Static image serving ──────────────────────────────────────────────────────

@customer_bp.route("/images/<path:filename>")
def serve_image(filename):
    """Serve car images from the project-level images/ directory."""
    images_dir = str(BASE_DIR / "images")
    return send_from_directory(images_dir, filename)


# ─── Home / Car Search ─────────────────────────────────────────────────────────

@customer_bp.route("/")
def index():
    """
    Landing page — shows available cars immediately.

    The sequence diagram starts here: Customer searches available cars,
    UI queries cars where availableNow = true, and displays the list.
    """
    cars = car_service.get_available_cars()
    return render_template("index.html", cars=cars)


@customer_bp.route("/cars")
def browse_cars():
    """Browse all available cars with optional category filter."""
    category = request.args.get("category", "")
    cars = car_service.get_available_cars()

    if category:
        cars = [c for c in cars if c.category.lower() == category.lower()]

    # Collect unique categories for the filter buttons
    all_cars = car_service.get_available_cars()
    categories = sorted(set(c.category for c in all_cars if c.category))

    return render_template("cars.html", cars=cars, categories=categories, selected_category=category)


@customer_bp.route("/cars/<car_id>")
def car_detail(car_id):
    """
    Car detail page — corresponds to viewCarDetails() in the class diagram
    and 'View Car Details' in the use case diagram.
    """
    car = car_service.get_car_by_id(car_id)
    if car is None:
        flash("Car not found.", "error")
        return redirect(url_for("customer.browse_cars"))
    return render_template("car_detail.html", car=car)


# ─── Authentication ────────────────────────────────────────────────────────────

@customer_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Customer registration — Login/Register use case.

    On GET: show the registration form.
    On POST: validate input, create the account, log in automatically.
    """
    # If already logged in, send them to the car listing
    if "customer_id" in session:
        return redirect(url_for("customer.index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        phone_no = request.form.get("phone_no", "").strip()
        license_id = request.form.get("license_id_no", "").strip()
        address = request.form.get("address", "").strip()

        # Basic form validation before hitting the service layer
        if not all([name, email, password, phone_no, license_id]):
            flash("Please fill in all required fields.", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("register.html")

        customer, error = customer_service.register_customer(
            name=name, email=email, password=password,
            phone_no=phone_no, license_id_no=license_id, address=address
        )

        if error:
            flash(error, "error")
            return render_template("register.html")

        # Log in automatically after registration
        session["customer_id"] = customer.id
        session["customer_name"] = customer.name
        flash(f"Welcome to Smriti Car Rental, {customer.name}!", "success")
        return redirect(url_for("customer.index"))

    return render_template("register.html")


@customer_bp.route("/login", methods=["GET", "POST"])
def login():
    """Customer login page."""
    if "customer_id" in session:
        return redirect(url_for("customer.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        customer = customer_service.authenticate_customer(email, password)
        if customer:
            session["customer_id"] = customer.id
            session["customer_name"] = customer.name
            flash(f"Welcome back, {customer.name}!", "success")
            return redirect(url_for("customer.index"))
        else:
            flash("Incorrect email or password. Please try again.", "error")

    return render_template("login.html")


@customer_bp.route("/logout")
def logout():
    """Clear the session and return to the home page."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("customer.index"))


# ─── Booking ───────────────────────────────────────────────────────────────────

@customer_bp.route("/book/<car_id>", methods=["GET", "POST"])
@customer_required
def book_car(car_id):
    """
    Booking form — Book/Reserve Car use case.

    GET: Show the booking form with date pickers and fee calculator.
    POST: Validate dates, check availability, calculate fee, store in session
          for the payment step.

    This implements sequence diagram steps 5–10:
    - Customer selects dates and books car (step 5)
    - Validate availability and rent period (step 6)
    - Return validation result (step 7)
    - Request fee calculation (step 8)
    - Return total fee (step 9)
    - Display fee summary (step 10)
    """
    car = car_service.get_car_by_id(car_id)
    if car is None:
        flash("Car not found.", "error")
        return redirect(url_for("customer.browse_cars"))

    if not car.available_now:
        flash("Sorry, this car is not currently available.", "warning")
        return redirect(url_for("customer.browse_cars"))

    if request.method == "POST":
        start_str = request.form.get("start_date", "")
        end_str = request.form.get("end_date", "")

        try:
            start_date = date.fromisoformat(start_str)
            end_date = date.fromisoformat(end_str)
        except ValueError:
            flash("Please enter valid dates.", "error")
            return render_template("booking.html", car=car, today=date.today().isoformat())

        # Validate through the booking engine — same logic as sequence diagram step 6
        valid, error = booking_engine.validate_availability(car, start_date, end_date)
        if not valid:
            flash(error, "error")
            return render_template("booking.html", car=car, today=date.today().isoformat())

        # Calculate the fee — sequence diagram step 8
        total_fee = booking_engine.calculate_total_fee(car.daily_rate, start_date, end_date)
        rental_days = (end_date - start_date).days

        # Store booking details in session so the payment page can use them
        session["pending_booking"] = {
            "car_id": car.id,
            "car_display_id": car.car_id,
            "car_name": f"{car.year} {car.make} {car.model}",
            "start_date": start_str,
            "end_date": end_str,
            "rental_days": rental_days,
            "daily_rate": car.daily_rate,
            "total_fee": total_fee
        }

        # Redirect to payment — sequence diagram step 10/11
        return redirect(url_for("customer.payment"))

    return render_template("booking.html", car=car, today=date.today().isoformat())


@customer_bp.route("/payment", methods=["GET", "POST"])
@customer_required
def payment():
    """
    Mock Stripe-style payment page — Make Payment use case.

    GET: Show the checkout form pre-filled with booking summary.
    POST: Process mock payment, create booking record, show pending notice.

    This implements sequence diagram steps 11–17:
    - Customer enters card details and pays (step 11)
    - Send transaction to payment gateway (step 12)
    - Return payment approval (step 13)
    - Create booking with PENDING status (step 14)
    - Save booking record (step 15)
    - Show booking pending notice (step 17)
    """
    booking_data = session.get("pending_booking")
    if not booking_data:
        flash("No active booking session. Please select a car and dates first.", "warning")
        return redirect(url_for("customer.browse_cars"))

    if request.method == "POST":
        card_number = request.form.get("card_number", "").strip()
        card_holder = request.form.get("card_holder", "").strip()
        expiry = request.form.get("expiry", "").strip()
        cvv = request.form.get("cvv", "").strip()

        # Basic card field validation
        cleaned_card = card_number.replace(" ", "").replace("-", "")
        if len(cleaned_card) < 13 or not cleaned_card.isdigit():
            flash("Please enter a valid card number.", "error")
            return render_template("payment.html", booking=booking_data)

        if not card_holder:
            flash("Please enter the cardholder name.", "error")
            return render_template("payment.html", booking=booking_data)

        if len(cvv) < 3:
            flash("Please enter a valid CVV.", "error")
            return render_template("payment.html", booking=booking_data)

        # Parse the dates back from the session strings
        start_date = date.fromisoformat(booking_data["start_date"])
        end_date = date.fromisoformat(booking_data["end_date"])

        # Create the booking and payment records
        booking, error = booking_engine.create_booking(
            customer_id=session["customer_id"],
            car_id=booking_data["car_id"],
            start_date=start_date,
            end_date=end_date,
            card_number=card_number,
            card_holder=card_holder
        )

        if error:
            flash(error, "error")
            return render_template("payment.html", booking=booking_data)

        # Clear the pending booking from the session — booking is now in the DB
        session.pop("pending_booking", None)

        flash("Payment processed successfully! Your booking is pending admin approval.", "success")
        return redirect(url_for("customer.booking_pending", booking_id=booking.booking_id))

    return render_template("payment.html", booking=booking_data)


@customer_bp.route("/booking/pending/<booking_id>")
@customer_required
def booking_pending(booking_id):
    """
    Booking pending confirmation page — sequence diagram step 17.
    'Engine → Customer: Show booking pending notice'
    """
    booking = db.session.query(Booking).filter_by(
        booking_id=booking_id,
        customer_id=session["customer_id"]
    ).first()

    if booking is None:
        flash("Booking not found.", "error")
        return redirect(url_for("customer.my_bookings"))

    return render_template("booking_pending.html", booking=booking)


@customer_bp.route("/my-bookings")
@customer_required
def my_bookings():
    """
    Customer's booking history page.

    Shows all bookings (pending, approved, rejected, cancelled)
    so the customer can track their reservation status.
    """
    bookings = db.session.query(Booking).filter_by(
        customer_id=session["customer_id"]
    ).order_by(Booking.created_at.desc()).all()

    return render_template("my_bookings.html", bookings=bookings)


@customer_bp.route("/cancel/<booking_id>", methods=["POST"])
@customer_required
def cancel_booking(booking_id):
    """
    Cancel a pending booking — Cancel Reservation use case.

    Customers can only cancel PENDING bookings. Once approved,
    they need to contact the company directly.
    """
    success, error = booking_engine.cancel_booking_by_customer(
        booking_id=booking_id,
        customer_id=session["customer_id"]
    )

    if success:
        flash("Your reservation has been cancelled.", "success")
    else:
        flash(error, "error")

    return redirect(url_for("customer.my_bookings"))
