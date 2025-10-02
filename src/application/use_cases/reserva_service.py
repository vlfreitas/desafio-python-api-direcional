from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.database.repositories import ReservaRepository, ApartamentoRepository, ClienteRepository
from src.infrastructure.database.models import Reserva
from src.infrastructure.database.models.apartamento import StatusApartamento
from src.application.dtos import ReservaCreate


class ReservaService:
    """Reserva service."""

    def __init__(self, db: Session):
        self.db = db
        self.reserva_repo = ReservaRepository(db)
        self.apartamento_repo = ApartamentoRepository(db)
        self.cliente_repo = ClienteRepository(db)

    def create_reserva(self, reserva_data: ReservaCreate) -> Reserva:
        """Create a new reserva."""
        # Verify cliente exists
        cliente = self.cliente_repo.get_by_id(reserva_data.cliente_id)
        if not cliente:
            raise ValueError("Cliente not found")

        # Verify apartamento exists
        apartamento = self.apartamento_repo.get_by_id(reserva_data.apartamento_id)
        if not apartamento:
            raise ValueError("Apartamento not found")

        # Check if apartamento is disponivel
        if apartamento.status != StatusApartamento.DISPONIVEL:
            raise ValueError("Apartamento is not available")

        # Check if apartamento already has an active reserva
        existing_reserva = self.reserva_repo.get_active_by_apartamento_id(reserva_data.apartamento_id)
        if existing_reserva:
            raise ValueError("Apartamento already has an active reservation")

        # Create reserva
        reserva = self.reserva_repo.create(reserva_data)

        # Update apartamento status to reservado
        self.apartamento_repo.update_status(reserva_data.apartamento_id, StatusApartamento.RESERVADO)

        return reserva

    def get_reserva(self, reserva_id: int) -> Optional[Reserva]:
        """Get a reserva by ID."""
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValueError("Reserva not found")
        return reserva

    def get_all_reservas(self, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Get all reservas."""
        return self.reserva_repo.get_all(skip, limit)

    def get_reservas_by_cliente(self, cliente_id: int, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Get reservas by cliente ID."""
        return self.reserva_repo.get_by_cliente_id(cliente_id, skip, limit)

    def cancel_reserva(self, reserva_id: int) -> bool:
        """Cancel a reserva."""
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValueError("Reserva not found")

        # Update reserva to inactive
        self.reserva_repo.update_ativa(reserva_id, False)

        # Update apartamento status back to disponivel
        self.apartamento_repo.update_status(reserva.apartamento_id, StatusApartamento.DISPONIVEL)

        return True

    def delete_reserva(self, reserva_id: int) -> bool:
        """Delete a reserva."""
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValueError("Reserva not found")

        # Update apartamento status back to disponivel if reserva is active
        if reserva.ativa:
            self.apartamento_repo.update_status(reserva.apartamento_id, StatusApartamento.DISPONIVEL)

        if not self.reserva_repo.delete(reserva_id):
            raise ValueError("Reserva not found")

        return True
