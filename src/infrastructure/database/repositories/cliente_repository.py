from typing import Optional, List
from sqlalchemy.orm import Session
from src.infrastructure.database.models import Cliente
from src.application.dtos import ClienteCreate, ClienteUpdate


class ClienteRepository:
    """Cliente repository."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente_data: ClienteCreate) -> Cliente:
        """Create a new cliente."""
        cliente = Cliente(**cliente_data.model_dump())
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """Get a cliente by ID."""
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_by_cpf(self, cpf: str) -> Optional[Cliente]:
        """Get a cliente by CPF."""
        return self.db.query(Cliente).filter(Cliente.cpf == cpf).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """Get all clientes."""
        return self.db.query(Cliente).offset(skip).limit(limit).all()

    def update(self, cliente_id: int, cliente_data: ClienteUpdate) -> Optional[Cliente]:
        """Update a cliente."""
        cliente = self.get_by_id(cliente_id)
        if not cliente:
            return None

        update_data = cliente_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(cliente, key, value)

        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def delete(self, cliente_id: int) -> bool:
        """Delete a cliente."""
        cliente = self.get_by_id(cliente_id)
        if not cliente:
            return False

        self.db.delete(cliente)
        self.db.commit()
        return True
