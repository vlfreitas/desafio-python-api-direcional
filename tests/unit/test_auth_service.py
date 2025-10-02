import pytest
from unittest.mock import Mock, MagicMock
from src.application.use_cases.auth_service import AuthService
from src.application.dtos import UserCreate, UserLogin
from src.infrastructure.database.models import Usuario


@pytest.mark.unit
def test_register_new_user():
    """Test registering a new user."""
    # Arrange
    mock_db = Mock()
    mock_repo = Mock()

    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )

    # Mock repository methods
    mock_repo.get_by_username.return_value = None
    mock_repo.get_by_email.return_value = None
    mock_repo.create.return_value = Usuario(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed"
    )

    # Act
    service = AuthService(mock_db)
    service.usuario_repo = mock_repo
    result = service.register(user_data)

    # Assert
    assert result.username == "testuser"
    mock_repo.get_by_username.assert_called_once_with("testuser")
    mock_repo.get_by_email.assert_called_once_with("test@example.com")
    mock_repo.create.assert_called_once()


@pytest.mark.unit
def test_register_duplicate_username():
    """Test registering with duplicate username."""
    # Arrange
    mock_db = Mock()
    mock_repo = Mock()

    user_data = UserCreate(
        username="existing",
        email="test@example.com",
        password="password123"
    )

    # Mock existing user
    mock_repo.get_by_username.return_value = Usuario(
        id=1,
        username="existing",
        email="other@example.com",
        hashed_password="hashed"
    )

    # Act & Assert
    service = AuthService(mock_db)
    service.usuario_repo = mock_repo

    with pytest.raises(ValueError, match="Username already exists"):
        service.register(user_data)


@pytest.mark.unit
def test_register_duplicate_email():
    """Test registering with duplicate email."""
    # Arrange
    mock_db = Mock()
    mock_repo = Mock()

    user_data = UserCreate(
        username="newuser",
        email="existing@example.com",
        password="password123"
    )

    # Mock no username conflict but email conflict
    mock_repo.get_by_username.return_value = None
    mock_repo.get_by_email.return_value = Usuario(
        id=1,
        username="other",
        email="existing@example.com",
        hashed_password="hashed"
    )

    # Act & Assert
    service = AuthService(mock_db)
    service.usuario_repo = mock_repo

    with pytest.raises(ValueError, match="Email already exists"):
        service.register(user_data)


@pytest.mark.unit
def test_authenticate_valid_credentials():
    """Test authentication with valid credentials."""
    # Arrange
    mock_db = Mock()
    mock_repo = Mock()

    login_data = UserLogin(username="testuser", password="password123")

    # Mock user with hashed password
    from src.infrastructure.auth import get_password_hash
    hashed = get_password_hash("password123")

    mock_repo.get_by_username.return_value = Usuario(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password=hashed,
        is_active=True
    )

    # Act
    service = AuthService(mock_db)
    service.usuario_repo = mock_repo
    token = service.authenticate(login_data)

    # Assert
    assert token is not None
    assert token.access_token is not None
    assert token.token_type == "bearer"


@pytest.mark.unit
def test_authenticate_invalid_username():
    """Test authentication with invalid username."""
    # Arrange
    mock_db = Mock()
    mock_repo = Mock()

    login_data = UserLogin(username="nonexistent", password="password123")
    mock_repo.get_by_username.return_value = None

    # Act
    service = AuthService(mock_db)
    service.usuario_repo = mock_repo
    token = service.authenticate(login_data)

    # Assert
    assert token is None


@pytest.mark.unit
def test_authenticate_invalid_password():
    """Test authentication with invalid password."""
    # Arrange
    mock_db = Mock()
    mock_repo = Mock()

    login_data = UserLogin(username="testuser", password="wrongpassword")

    from src.infrastructure.auth import get_password_hash
    hashed = get_password_hash("correctpassword")

    mock_repo.get_by_username.return_value = Usuario(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password=hashed,
        is_active=True
    )

    # Act
    service = AuthService(mock_db)
    service.usuario_repo = mock_repo
    token = service.authenticate(login_data)

    # Assert
    assert token is None


@pytest.mark.unit
def test_authenticate_inactive_user():
    """Test authentication with inactive user."""
    # Arrange
    mock_db = Mock()
    mock_repo = Mock()

    login_data = UserLogin(username="testuser", password="password123")

    from src.infrastructure.auth import get_password_hash
    hashed = get_password_hash("password123")

    mock_repo.get_by_username.return_value = Usuario(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password=hashed,
        is_active=False  # Inactive user
    )

    # Act
    service = AuthService(mock_db)
    service.usuario_repo = mock_repo
    token = service.authenticate(login_data)

    # Assert
    assert token is None
