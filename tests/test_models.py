from app.models import Admin, Booking, Car, Customer, Payment


def test_customer_password_hashing(customer_app):
    with customer_app.app_context():
        customer = Customer(name="Test", email="test@test.com", phone_no="123", license_id_no="123")
        customer.set_password("mypassword")
        assert customer.password_hash != "mypassword"
        assert customer.check_password("mypassword") is True
        assert customer.check_password("wrongpassword") is False

def test_admin_password_hashing(admin_app):
    with admin_app.app_context():
        admin = Admin(employee_id="123", name="Test", email="test@test.com")
        admin.set_password("adminpass")
        assert admin.password_hash != "adminpass"
        assert admin.check_password("adminpass") is True

def test_car_mileage_update(customer_app):
    with customer_app.app_context():
        car = Car(car_id="C1", make="Ford", model="Focus", year=2020, daily_rate=40, mileage=100)
        car.update_mileage(150)
        assert car.mileage == 150
        
        # Mileage cannot decrease
        car.update_mileage(120)
        assert car.mileage == 150

def test_booking_fee_calculation(customer_app):
    with customer_app.app_context():
        booking = Booking(booking_id="TEST", customer_id=1, car_id=1,
                          total_fee=0.0)
        fee = booking.calculate_total_fee(50.0, 3)
        assert fee == 150.0

def test_payment_processing(customer_app):
    with customer_app.app_context():
        payment = Payment(payment_id="P1", booking_id=1, amount=100.0)
        payment.process_credit_card("1111222233334444", "John Doe")
        assert payment.payment_status == "COMPLETED"
        assert payment.card_last_four == "4444"
        assert payment.card_holder_name == "John Doe"
