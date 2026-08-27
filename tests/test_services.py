from datetime import date, timedelta
from app.services import booking_engine, car_service
from app.models.booking import STATUS_PENDING, STATUS_APPROVED

def test_validate_availability_valid(customer_app, sample_car):
    with customer_app.app_context():
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        valid, msg = booking_engine.validate_availability(sample_car, start, end)
        assert valid is True
        assert msg == ""

def test_validate_availability_past_date(customer_app, sample_car):
    with customer_app.app_context():
        start = date.today() - timedelta(days=1)
        end = date.today() + timedelta(days=2)
        valid, msg = booking_engine.validate_availability(sample_car, start, end)
        assert valid is False
        assert "past" in msg

def test_validate_availability_car_unavailable(customer_app, sample_car):
    with customer_app.app_context():
        sample_car.available_now = False
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        valid, msg = booking_engine.validate_availability(sample_car, start, end)
        assert valid is False
        assert "not currently available" in msg

def test_create_and_approve_booking(customer_app, sample_customer, sample_car):
    with customer_app.app_context():
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        
        booking, msg = booking_engine.create_booking(
            sample_customer.id, sample_car.id, start, end, "1111222233334444", "John Doe"
        )
        
        assert booking is not None
        assert booking.booking_status == STATUS_PENDING
        assert booking.payment is not None
        
        # Now approve it
        success, err = booking_engine.approve_booking(booking.booking_id, "All good")
        assert success is True
        
        # Check that car is marked unavailable
        assert sample_car.available_now is False
        assert booking.booking_status == STATUS_APPROVED
