from typing import Optional, List
from sqlalchemy.orm import Session
from src.infrastructure.database.models import Venda
from src.application.dtos import VendaCreate


class VendaRepository:
    """Venda repository."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, venda_data: VendaCreate) -> Venda:
        """Create a new venda."""
        venda = Venda(**venda_data.model_dump())
        self.db.add(venda)
        self.db.commit()
        self.db.refresh(venda)
        return venda

    def get_by_id(self, venda_id: int) -> Optional[Venda]:
        """Get a venda by ID."""
        return self.db.query(Venda).filter(Venda.id == venda_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Venda]:
        """Get all vendas."""
        return self.db.query(Venda).offset(skip).limit(limit).all()

    def get_by_cliente_id(self, cliente_id: int, skip: int = 0, limit: int = 100) -> List[Venda]:
        """Get vendas by cliente ID."""
        return self.db.query(Venda).filter(Venda.cliente_id == cliente_id).offset(skip).limit(limit).all()

    def get_by_apartamento_id(self, apartamento_id: int) -> Optional[Venda]:
        """Get venda by apartamento ID."""
        return self.db.query(Venda).filter(Venda.apartamento_id == apartamento_id).first()

    def delete(self, venda_id: int) -> bool:
        """Delete a venda."""
        venda = self.get_by_id(venda_id)
        if not venda:
            return False

        self.db.delete(venda)
        self.db.commit()
        return True
