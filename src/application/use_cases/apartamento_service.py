from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.database.repositories import ApartamentoRepository
from src.infrastructure.database.models import Apartamento
from src.infrastructure.database.models.apartamento import StatusApartamento
from src.application.dtos import ApartamentoCreate, ApartamentoUpdate


class ApartamentoService:
    """Apartamento service."""

    def __init__(self, db: Session):
        self.db = db
        self.apartamento_repo = ApartamentoRepository(db)

    def create_apartamento(self, apartamento_data: ApartamentoCreate) -> Apartamento:
        """Create a new apartamento."""
        # Check if numero already exists
        if self.apartamento_repo.get_by_numero(apartamento_data.numero):
            raise ValueError("Apartamento number already exists")

        return self.apartamento_repo.create(apartamento_data)

    def get_apartamento(self, apartamento_id: int) -> Optional[Apartamento]:
        """Get an apartamento by ID."""
        apartamento = self.apartamento_repo.get_by_id(apartamento_id)
        if not apartamento:
            raise ValueError("Apartamento not found")
        return apartamento

    def get_all_apartamentos(self, skip: int = 0, limit: int = 100) -> List[Apartamento]:
        """Get all apartamentos."""
        return self.apartamento_repo.get_all(skip, limit)

    def get_apartamentos_by_status(
        self, status: StatusApartamento, skip: int = 0, limit: int = 100
    ) -> List[Apartamento]:
        """Get apartamentos by status."""
        return self.apartamento_repo.get_by_status(status, skip, limit)

    def update_apartamento(
        self, apartamento_id: int, apartamento_data: ApartamentoUpdate
    ) -> Apartamento:
        """Update an apartamento."""
        apartamento = self.apartamento_repo.update(apartamento_id, apartamento_data)
        if not apartamento:
            raise ValueError("Apartamento not found")
        return apartamento

    def delete_apartamento(self, apartamento_id: int) -> bool:
        """Delete an apartamento."""
        if not self.apartamento_repo.delete(apartamento_id):
            raise ValueError("Apartamento not found")
        return True

    def check_disponibilidade(self, apartamento_id: int) -> bool:
        """Check if apartamento is available."""
        apartamento = self.get_apartamento(apartamento_id)
        return apartamento.status == StatusApartamento.DISPONIVEL
