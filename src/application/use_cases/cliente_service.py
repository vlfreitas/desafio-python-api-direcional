from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.database.repositories import ClienteRepository
from src.infrastructure.database.models import Cliente
from src.application.dtos import ClienteCreate, ClienteUpdate


class ClienteService:
    """Cliente service."""

    def __init__(self, db: Session):
        self.db = db
        self.cliente_repo = ClienteRepository(db)

    def create_cliente(self, cliente_data: ClienteCreate) -> Cliente:
        """Create a new cliente."""
        # Check if CPF already exists
        if self.cliente_repo.get_by_cpf(cliente_data.cpf):
            raise ValueError("CPF already exists")

        return self.cliente_repo.create(cliente_data)

    def get_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """Get a cliente by ID."""
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente not found")
        return cliente

    def get_all_clientes(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """Get all clientes."""
        return self.cliente_repo.get_all(skip, limit)

    def update_cliente(self, cliente_id: int, cliente_data: ClienteUpdate) -> Cliente:
        """Update a cliente."""
        cliente = self.cliente_repo.update(cliente_id, cliente_data)
        if not cliente:
            raise ValueError("Cliente not found")
        return cliente

    def delete_cliente(self, cliente_id: int) -> bool:
        """Delete a cliente."""
        if not self.cliente_repo.delete(cliente_id):
            raise ValueError("Cliente not found")
        return True
