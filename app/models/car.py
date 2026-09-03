"""
Car model — represents a vehicle available for rental.

This maps to the Car class in the class diagram:
  - carId, make, model, year, mileage, availableNow,
    minRentPeriod, maxRentPeriod, dailyRate, image

The image field stores the path relative to the project root,
for example: images/toyota-camry.jpg
"""

from datetime import datetime
from database import db


class Car(db.Model):
    """
    A vehicle in the fleet that customers can browse and book.

    availableNow is the key flag used in the sequence diagram:
      - The UI queries cars where availableNow = true when searching.
      - When admin approves a booking, the engine sets availableNow = false.
    """

    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)

    # The car_id is a human-readable identifier like "CAR-001"
    car_id = db.Column(db.String(20), unique=True, nullable=False)

    make = db.Column(db.String(50), nullable=False)   # e.g. Toyota
    model = db.Column(db.String(50), nullable=False)  # e.g. Camry
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Float, default=0.0)

    # This flag is the one checked during the sequence diagram search step
    available_now = db.Column(db.Boolean, default=True, nullable=False)

    # Per-car rental period constraints — the booking engine checks these
    min_rent_period = db.Column(db.Integer, default=1)   # days
    max_rent_period = db.Column(db.Integer, default=30)  # days

    daily_rate = db.Column(db.Float, nullable=False)

    # Path to the local image file, e.g. "images/toyota-camry.jpg"
    image = db.Column(db.String(200), nullable=True)

    # A brief description helps customers understand the car
    description = db.Column(db.Text, nullable=True)

    # Category helps with filtering: economy, sedan, SUV, luxury, etc.
    category = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # One car can appear in many bookings over time
    bookings = db.relationship("Booking", backref="car", lazy=True)

    # Per-car optional/mandatory extra charges (GPS, insurance, etc.)
    additional_charges = db.relationship("AdditionalCharge", backref="car", lazy=True, cascade="all, delete-orphan")


    def update_mileage(self, new_mileage: float) -> None:
        """
        Update the odometer reading.

        We only allow mileage to increase — you can't roll back the odometer.
        """
        if new_mileage >= self.mileage:
            self.mileage = new_mileage

    def set_availability(self, status: bool) -> None:
        """
        Mark the car as available or unavailable.

        This is called by the booking engine when admin approves a booking
        (sets to False) or when a booking ends (sets back to True).
        """
        self.available_now = status

    def __repr__(self) -> str:
        status = "available" if self.available_now else "booked"
        return f"<Car {self.car_id}: {self.year} {self.make} {self.model} ({status})>"
