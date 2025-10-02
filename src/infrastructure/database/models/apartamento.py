from typing import List, Optional
from sqlalchemy import String, Integer, Numeric, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from .base import Base


class StatusApartamento(str, enum.Enum):
    """Status do apartamento."""

    DISPONIVEL = "disponivel"
    RESERVADO = "reservado"
    VENDIDO = "vendido"


class Apartamento(Base):
    """Apartamento model."""

    __tablename__ = "apartamentos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    numero: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    bloco: Mapped[str] = mapped_column(String(10), nullable=False)
    andar: Mapped[int] = mapped_column(Integer, nullable=False)
    quartos: Mapped[int] = mapped_column(Integer, nullable=False)
    area: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    preco: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    status: Mapped[StatusApartamento] = mapped_column(
        SQLEnum(StatusApartamento), default=StatusApartamento.DISPONIVEL, nullable=False
    )

    # Relationships
    vendas: Mapped[List["Venda"]] = relationship(
        "Venda", back_populates="apartamento", cascade="all, delete-orphan"
    )
    reservas: Mapped[List["Reserva"]] = relationship(
        "Reserva", back_populates="apartamento", cascade="all, delete-orphan"
    )
