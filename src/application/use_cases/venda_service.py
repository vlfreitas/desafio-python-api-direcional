from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.database.repositories import VendaRepository, ApartamentoRepository, ClienteRepository
from src.infrastructure.database.models import Venda
from src.infrastructure.database.models.apartamento import StatusApartamento
from src.application.dtos import VendaCreate


class VendaService:
    """Venda service."""

    def __init__(self, db: Session):
        self.db = db
        self.venda_repo = VendaRepository(db)
        self.apartamento_repo = ApartamentoRepository(db)
        self.cliente_repo = ClienteRepository(db)

    def create_venda(self, venda_data: VendaCreate) -> Venda:
        """Create a new venda."""
        # Verify cliente exists
        cliente = self.cliente_repo.get_by_id(venda_data.cliente_id)
        if not cliente:
            raise ValueError("Cliente not found")

        # Verify apartamento exists
        apartamento = self.apartamento_repo.get_by_id(venda_data.apartamento_id)
        if not apartamento:
            raise ValueError("Apartamento not found")

        # Check if apartamento is disponivel or reservado
        if apartamento.status not in [StatusApartamento.DISPONIVEL, StatusApartamento.RESERVADO]:
            raise ValueError("Apartamento is not available for sale")

        # Check if apartamento already has a venda
        existing_venda = self.venda_repo.get_by_apartamento_id(venda_data.apartamento_id)
        if existing_venda:
            raise ValueError("Apartamento already sold")

        # Create venda
        venda = self.venda_repo.create(venda_data)

        # Update apartamento status to vendido
        self.apartamento_repo.update_status(venda_data.apartamento_id, StatusApartamento.VENDIDO)

        return venda

    def get_venda(self, venda_id: int) -> Optional[Venda]:
        """Get a venda by ID."""
        venda = self.venda_repo.get_by_id(venda_id)
        if not venda:
            raise ValueError("Venda not found")
        return venda

    def get_all_vendas(self, skip: int = 0, limit: int = 100) -> List[Venda]:
        """Get all vendas."""
        return self.venda_repo.get_all(skip, limit)

    def get_vendas_by_cliente(self, cliente_id: int, skip: int = 0, limit: int = 100) -> List[Venda]:
        """Get vendas by cliente ID."""
        return self.venda_repo.get_by_cliente_id(cliente_id, skip, limit)

    def delete_venda(self, venda_id: int) -> bool:
        """Delete a venda."""
        venda = self.venda_repo.get_by_id(venda_id)
        if not venda:
            raise ValueError("Venda not found")

        # Update apartamento status back to disponivel
        self.apartamento_repo.update_status(venda.apartamento_id, StatusApartamento.DISPONIVEL)

        if not self.venda_repo.delete(venda_id):
            raise ValueError("Venda not found")

        return True
