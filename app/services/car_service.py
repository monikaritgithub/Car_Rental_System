"""
Car service — CRUD operations for managing vehicles in the fleet.

This implements the Admin use cases from the use case diagram:
  - addCar()
  - updateCar()
  - deleteCar()

And the Customer use case:
  - searchCars() — returns only cars where availableNow = true
  - viewCarDetails() — returns a single car by its car_id
"""

from typing import Optional
from database import db
from app.models.car import Car


def _generate_car_id() -> str:
    """Generate the next sequential car ID, e.g. CAR-001."""
    count = db.session.query(Car).count()
    return f"CAR-{count + 1:03d}"


def get_available_cars() -> list[Car]:
    """
    Return all cars where availableNow = true.

    This is sequence diagram step 2:
    'UI → DB: Query cars where availableNow = true'
    """
    return db.session.query(Car).filter_by(available_now=True).order_by(Car.make, Car.model).all()


def get_all_cars() -> list[Car]:
    """
    Return every car in the fleet regardless of availability.

    This is used by the admin interface which needs to see all cars,
    including ones that are currently out on rental.
    """
    return db.session.query(Car).order_by(Car.make, Car.model).all()


def get_car_by_id(car_id: str) -> Optional[Car]:
    """
    Look up a car by its human-readable ID like 'CAR-001'.

    Returns None if not found.
    """
    return db.session.query(Car).filter_by(car_id=car_id).first()


def get_car_by_pk(pk: int) -> Optional[Car]:
    """Look up a car by its database primary key."""
    return db.session.get(Car, pk)


def add_car(make: str, model: str, year: int, mileage: float,
            daily_rate: float, min_rent: int, max_rent: int,
            image: str = "", description: str = "",
            category: str = "") -> Car:
    """
    Add a new car to the fleet.

    This corresponds to the Admin.addCar() method in the class diagram
    and the 'Add Car' use case in the use case diagram.
    """
    car = Car(
        car_id=_generate_car_id(),
        make=make.strip(),
        model=model.strip(),
        year=year,
        mileage=mileage,
        daily_rate=daily_rate,
        min_rent_period=min_rent,
        max_rent_period=max_rent,
        image=image.strip() if image else "",
        description=description.strip() if description else "",
        category=category.strip() if category else "",
        available_now=True
    )
    db.session.add(car)
    db.session.commit()
    return car


def update_car(car_id: str, **kwargs) -> tuple[bool, str]:
    """
    Update an existing car's details.

    Only the fields provided in kwargs are changed. This lets admin
    update just the daily rate, for example, without touching other fields.
    """
    car = get_car_by_id(car_id)
    if car is None:
        return False, f"Car with ID {car_id} not found."

    allowed_fields = {
        "make", "model", "year", "mileage", "daily_rate",
        "min_rent_period", "max_rent_period", "image",
        "description", "category", "available_now"
    }

    for field, value in kwargs.items():
        if field in allowed_fields:
            setattr(car, field, value)

    db.session.commit()
    return True, ""


def delete_car(car_id: str) -> tuple[bool, str]:
    """
    Remove a car from the fleet.

    We don't allow deletion if the car has any active (PENDING or APPROVED)
    bookings — that would leave customers with a missing reservation.
    """
    from app.models.booking import Booking, STATUS_PENDING, STATUS_APPROVED

    car = get_car_by_id(car_id)
    if car is None:
        return False, f"Car with ID {car_id} not found."

    # Check for active bookings before deleting
    active_booking = db.session.query(Booking).filter(
        Booking.car_id == car.id,
        Booking.booking_status.in_([STATUS_PENDING, STATUS_APPROVED])
    ).first()

    if active_booking:
        return False, "This car has active bookings and cannot be deleted."

    db.session.delete(car)
    db.session.commit()
    return True, ""
