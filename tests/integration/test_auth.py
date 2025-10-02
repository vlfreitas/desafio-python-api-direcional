import pytest


@pytest.mark.integration
def test_register_user(client):
    """Test user registration."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "pass123",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"


@pytest.mark.integration
def test_register_duplicate_username(client):
    """Test registration with duplicate username."""
    user_data = {
        "username": "duplicate",
        "email": "user1@example.com",
        "password": "pass123",
    }
    client.post("/auth/register", json=user_data)

    # Try to register again with same username
    user_data2 = {
        "username": "duplicate",
        "email": "user2@example.com",
        "password": "pass123",
    }
    response = client.post("/auth/register", json=user_data2)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.integration
def test_login(client):
    """Test user login."""
    # Register user
    user_data = {
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "pass123",
    }
    client.post("/auth/register", json=user_data)

    # Login
    login_data = {"username": "loginuser", "password": "pass123"}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.integration
def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    login_data = {"username": "nonexistent", "password": "wrong"}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
