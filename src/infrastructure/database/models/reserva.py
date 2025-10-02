from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Reserva(Base):
    """Reserva model."""

    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    apartamento_id: Mapped[int] = mapped_column(
        ForeignKey("apartamentos.id"), nullable=False
    )
    data_reserva: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    data_expiracao: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ativa: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Relationships
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="reservas")
    apartamento: Mapped["Apartamento"] = relationship(
        "Apartamento", back_populates="reservas"
    )
