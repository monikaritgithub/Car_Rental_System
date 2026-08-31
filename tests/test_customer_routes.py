def test_index_page(customer_client):
    response = customer_client.get("/")
    assert response.status_code == 200
    assert b"Save up to 20%" in response.data

def test_browse_cars(customer_client, sample_car):
    response = customer_client.get("/cars")
    assert response.status_code == 200
    assert b"TestMake TestModel" in response.data

def test_login_page_renders(customer_client):
    response = customer_client.get("/login")
    assert response.status_code == 200
    assert b"Sign in" in response.data

def test_login_post(customer_client, sample_customer):
    response = customer_client.post("/login", data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome back" in response.data

def test_booking_requires_login(customer_client, sample_car):
    response = customer_client.get(f"/book/{sample_car.car_id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in" in response.data
