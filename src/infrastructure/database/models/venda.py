from datetime import datetime
from sqlalchemy import ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Venda(Base):
    """Venda model."""

    __tablename__ = "vendas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    apartamento_id: Mapped[int] = mapped_column(
        ForeignKey("apartamentos.id"), nullable=False
    )
    valor_venda: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    valor_entrada: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    data_venda: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="vendas")
    apartamento: Mapped["Apartamento"] = relationship(
        "Apartamento", back_populates="vendas"
    )
