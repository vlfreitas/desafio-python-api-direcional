import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from src.infrastructure.database.models import Base
from src.main import app
from src.infrastructure.database import get_db

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token(client):
    """Create a user and return an auth token."""
    # Register user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123",
    }
    client.post("/auth/register", json=user_data)

    # Login to get token
    login_data = {"username": "testuser", "password": "test123"}
    response = client.post("/auth/login", data=login_data)
    return response.json()["access_token"]
