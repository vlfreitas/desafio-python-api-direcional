from typing import Optional, List
from sqlalchemy.orm import Session
from src.infrastructure.database.models import Apartamento
from src.infrastructure.database.models.apartamento import StatusApartamento
from src.application.dtos import ApartamentoCreate, ApartamentoUpdate


class ApartamentoRepository:
    """Apartamento repository."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, apartamento_data: ApartamentoCreate) -> Apartamento:
        """Create a new apartamento."""
        apartamento = Apartamento(**apartamento_data.model_dump())
        self.db.add(apartamento)
        self.db.commit()
        self.db.refresh(apartamento)
        return apartamento

    def get_by_id(self, apartamento_id: int) -> Optional[Apartamento]:
        """Get an apartamento by ID."""
        return self.db.query(Apartamento).filter(Apartamento.id == apartamento_id).first()

    def get_by_numero(self, numero: str) -> Optional[Apartamento]:
        """Get an apartamento by numero."""
        return self.db.query(Apartamento).filter(Apartamento.numero == numero).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Apartamento]:
        """Get all apartamentos."""
        return self.db.query(Apartamento).offset(skip).limit(limit).all()

    def get_by_status(self, status: StatusApartamento, skip: int = 0, limit: int = 100) -> List[Apartamento]:
        """Get apartamentos by status."""
        return self.db.query(Apartamento).filter(Apartamento.status == status).offset(skip).limit(limit).all()

    def update(self, apartamento_id: int, apartamento_data: ApartamentoUpdate) -> Optional[Apartamento]:
        """Update an apartamento."""
        apartamento = self.get_by_id(apartamento_id)
        if not apartamento:
            return None

        update_data = apartamento_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(apartamento, key, value)

        self.db.commit()
        self.db.refresh(apartamento)
        return apartamento

    def delete(self, apartamento_id: int) -> bool:
        """Delete an apartamento."""
        apartamento = self.get_by_id(apartamento_id)
        if not apartamento:
            return False

        self.db.delete(apartamento)
        self.db.commit()
        return True

    def update_status(self, apartamento_id: int, status: StatusApartamento) -> Optional[Apartamento]:
        """Update apartamento status."""
        apartamento = self.get_by_id(apartamento_id)
        if not apartamento:
            return None

        apartamento.status = status
        self.db.commit()
        self.db.refresh(apartamento)
        return apartamento
