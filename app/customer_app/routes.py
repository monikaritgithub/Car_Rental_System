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

from functools import wraps

from database import db
from app.models.booking import Booking
from app.services import car_service, customer_service, booking_engine
from app.services.recommendation_service import recommend_cars
from flask import jsonify
from config.settings import BASE_DIR

# All customer routes live under this blueprint
customer_bp = Blueprint("customer", __name__)


# ─── Helper ────────────────────────────────────────────────────────────────────

def customer_required(f):
    """
    Decorator that redirects to the login page if no customer is signed in.
    
    Uses a simple session-based approach to check if the customer is logged in.
    """
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
    """
    cars = car_service.get_available_cars()
    return render_template("index.html", cars=cars)


# ─── Static Info Pages (formerly broken #-links in navbar) ────────────────────

@customer_bp.route("/smriti-zero")
def smriti_zero():
    """Smriti Zero — electric and hybrid fleet showcase page."""
    return render_template("smriti_zero.html")


@customer_bp.route("/locations")
def locations():
    """Branch locations across New Zealand."""
    return render_template("locations.html")


@customer_bp.route("/deals")
def deals():
    """Current promotions and discount offers."""
    return render_template("deals.html")


@customer_bp.route("/about")
def about():
    """Company information, story, and contact details."""
    return render_template("about.html")


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
    Car detail page — shows specifications and booking form.
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
    Customer registration.
    
    GET: Display the registration form.
    POST: Process registration, handle validation, and log the user in automatically.
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
    Booking form — Handle car reservations.

    GET: Show the booking form with date pickers.
    POST: Validate dates and availability, calculate total fee, and prepare session for payment.
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

        # Check if the car is available for the requested dates
        valid, error = booking_engine.validate_availability(car, start_date, end_date)
        if not valid:
            flash(error, "error")
            return render_template("booking.html", car=car, today=date.today().isoformat())

        # Calculate the total rental fee and itemized breakdown
        total_fee, breakdown = booking_engine.calculate_total_fee(car.daily_rate, start_date, end_date, car)
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
            "total_fee": total_fee,
            "breakdown": breakdown
        }

        # Proceed to payment step
        return redirect(url_for("customer.payment"))

    return render_template("booking.html", car=car, today=date.today().isoformat())


@customer_bp.route("/payment", methods=["GET", "POST"])
@customer_required
def payment():
    """
    Mock Stripe-style payment page.

    GET: Show the checkout form with a booking summary.
    POST: Process payment, create the booking, and display confirmation.
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

        # Clear the pending booking from the session since it's now saved in the database
        session.pop("pending_booking", None)

        flash("Payment processed successfully! Your booking is pending admin approval.", "success")
        return redirect(url_for("customer.booking_pending", booking_id=booking.booking_id))

    return render_template("payment.html", booking=booking_data)


@customer_bp.route("/booking/pending/<booking_id>")
@customer_required
def booking_pending(booking_id):
    """
    Booking pending confirmation page.
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
    """View the logged-in customer's booking history."""
    customer_id = session["customer_id"]
    bookings = db.session.query(Booking).filter_by(customer_id=customer_id).order_by(Booking.created_at.desc()).all()
    return render_template("my_bookings.html", bookings=bookings)


@customer_bp.route("/cancel-booking/<booking_id>", methods=["POST"])
@customer_required
def cancel_booking(booking_id):
    """
    Customer cancels their own pending booking.
    """
    customer_id = session["customer_id"]
    success, error = booking_engine.cancel_booking_by_customer(booking_id, customer_id)

    if success:
        flash(f"Booking {booking_id} has been cancelled successfully.", "success")
    else:
        flash(error, "error")

    return redirect(url_for("customer.my_bookings"))


# ─── API Routes (AJAX) ────────────────────────────────────────────────────────

@customer_bp.route("/api/recommend", methods=["POST"])
def api_recommend_cars():
    """
    API endpoint for the AI Car Recommendation widget.
    Takes JSON payload with user preferences and returns recommended cars.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        passengers = int(data.get("passengers", 2))
        budget = float(data.get("budget", 100.0))
        purpose = data.get("purpose", "city")
        days = int(data.get("days", 3))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input format"}), 400

    results = recommend_cars(passengers, budget, purpose, days)

    # Format for JSON response
    response = []
    for r in results:
        car = r["car"]
        response.append({
            "car_id": car.car_id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "category": car.category,
            "daily_rate": car.daily_rate,
            "image": car.image,
            "score": r["score"],
            "reasons": r["reasons"]
        })

    return jsonify({"recommendations": response})
