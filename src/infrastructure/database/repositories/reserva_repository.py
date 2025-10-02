from typing import Optional, List
from sqlalchemy.orm import Session
from src.infrastructure.database.models import Reserva
from src.application.dtos import ReservaCreate


class ReservaRepository:
    """Reserva repository."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, reserva_data: ReservaCreate) -> Reserva:
        """Create a new reserva."""
        reserva = Reserva(**reserva_data.model_dump())
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def get_by_id(self, reserva_id: int) -> Optional[Reserva]:
        """Get a reserva by ID."""
        return self.db.query(Reserva).filter(Reserva.id == reserva_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Get all reservas."""
        return self.db.query(Reserva).offset(skip).limit(limit).all()

    def get_by_cliente_id(self, cliente_id: int, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Get reservas by cliente ID."""
        return self.db.query(Reserva).filter(Reserva.cliente_id == cliente_id).offset(skip).limit(limit).all()

    def get_active_by_apartamento_id(self, apartamento_id: int) -> Optional[Reserva]:
        """Get active reserva by apartamento ID."""
        return (
            self.db.query(Reserva)
            .filter(Reserva.apartamento_id == apartamento_id, Reserva.ativa == True)
            .first()
        )

    def update_ativa(self, reserva_id: int, ativa: bool) -> Optional[Reserva]:
        """Update reserva ativa status."""
        reserva = self.get_by_id(reserva_id)
        if not reserva:
            return None

        reserva.ativa = ativa
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def delete(self, reserva_id: int) -> bool:
        """Delete a reserva."""
        reserva = self.get_by_id(reserva_id)
        if not reserva:
            return False

        self.db.delete(reserva)
        self.db.commit()
        return True
