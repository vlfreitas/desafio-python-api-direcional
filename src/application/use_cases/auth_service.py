from typing import Optional
from sqlalchemy.orm import Session
from src.infrastructure.database.repositories import UsuarioRepository
from src.infrastructure.auth import verify_password, create_access_token
from src.application.dtos import UserCreate, UserLogin, Token


class AuthService:
    """Authentication service."""

    def __init__(self, db: Session):
        self.db = db
        self.usuario_repo = UsuarioRepository(db)

    def register(self, user_data: UserCreate):
        """Register a new user."""
        # Check if username already exists
        if self.usuario_repo.get_by_username(user_data.username):
            raise ValueError("Username already exists")

        # Check if email already exists
        if self.usuario_repo.get_by_email(user_data.email):
            raise ValueError("Email already exists")

        # Create user
        return self.usuario_repo.create(user_data)

    def authenticate(self, user_data: UserLogin) -> Optional[Token]:
        """Authenticate a user and return a token."""
        user = self.usuario_repo.get_by_username(user_data.username)
        if not user:
            return None

        if not user.is_active:
            return None

        if not verify_password(user_data.password, user.hashed_password):
            return None

        access_token = create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")

    def get_user_by_username(self, username: str):
        """Get user by username."""
        return self.usuario_repo.get_by_username(username)
