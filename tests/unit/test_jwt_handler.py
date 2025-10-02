import pytest
from datetime import timedelta
from src.infrastructure.auth.jwt_handler import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
)


@pytest.mark.unit
def test_password_hashing():
    """Test password hashing."""
    password = "mypassword123"
    hashed = get_password_hash(password)

    # Hash should be different from original
    assert hashed != password
    # Hash should be consistent format (bcrypt)
    assert hashed.startswith("$2b$")


@pytest.mark.unit
def test_verify_password_correct():
    """Test verifying correct password."""
    password = "mypassword123"
    hashed = get_password_hash(password)

    assert verify_password(password, hashed) is True


@pytest.mark.unit
def test_verify_password_incorrect():
    """Test verifying incorrect password."""
    password = "mypassword123"
    wrong_password = "wrongpassword"
    hashed = get_password_hash(password)

    assert verify_password(wrong_password, hashed) is False


@pytest.mark.unit
def test_create_access_token():
    """Test creating access token."""
    data = {"sub": "testuser"}
    token = create_access_token(data)

    # Token should be a non-empty string
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.unit
def test_create_access_token_with_expiration():
    """Test creating access token with custom expiration."""
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta)

    # Token should be valid
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.unit
def test_decode_access_token():
    """Test decoding access token."""
    data = {"sub": "testuser"}
    token = create_access_token(data)

    username = decode_access_token(token)

    assert username == "testuser"


@pytest.mark.unit
def test_decode_invalid_token():
    """Test decoding invalid token."""
    invalid_token = "invalid.token.here"

    username = decode_access_token(invalid_token)

    assert username is None


@pytest.mark.unit
def test_decode_expired_token():
    """Test decoding expired token."""
    data = {"sub": "testuser"}
    # Create token that expires immediately
    expires_delta = timedelta(seconds=-1)
    token = create_access_token(data, expires_delta)

    username = decode_access_token(token)

    assert username is None


@pytest.mark.unit
def test_different_passwords_different_hashes():
    """Test that different passwords produce different hashes."""
    password1 = "password123"
    password2 = "password456"

    hash1 = get_password_hash(password1)
    hash2 = get_password_hash(password2)

    assert hash1 != hash2


@pytest.mark.unit
def test_same_password_different_hashes():
    """Test that same password hashed twice produces different hashes (salt)."""
    password = "password123"

    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Hashes should be different due to random salt
    assert hash1 != hash2
    # But both should verify correctly
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)
