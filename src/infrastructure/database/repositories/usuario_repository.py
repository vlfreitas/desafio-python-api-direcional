from typing import Optional
from sqlalchemy.orm import Session
from src.infrastructure.database.models import Usuario
from src.application.dtos import UserCreate
from src.infrastructure.auth import get_password_hash


class UsuarioRepository:
    """Usuario repository."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: UserCreate) -> Usuario:
        """Create a new usuario."""
        hashed_password = get_password_hash(user_data.password)
        usuario = Usuario(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def get_by_username(self, username: str) -> Optional[Usuario]:
        """Get a usuario by username."""
        return self.db.query(Usuario).filter(Usuario.username == username).first()

    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Get a usuario by email."""
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Get a usuario by ID."""
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
