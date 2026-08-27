def test_admin_login_renders(admin_client):
    response = admin_client.get("/login")
    assert response.status_code == 200
    assert b"Admin Portal" in response.data

def test_admin_login_post(admin_client, sample_admin):
    response = admin_client.post("/login", data={
        "email": "admin@example.com",
        "password": "admin123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Dashboard Overview" in response.data

def test_dashboard_requires_login(admin_client):
    response = admin_client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Admin login required." in response.data
