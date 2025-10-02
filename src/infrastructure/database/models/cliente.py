from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Cliente(Base):
    """Cliente model."""

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)

    # Relationships
    vendas: Mapped[List["Venda"]] = relationship(
        "Venda", back_populates="cliente", cascade="all, delete-orphan"
    )
    reservas: Mapped[List["Reserva"]] = relationship(
        "Reserva", back_populates="cliente", cascade="all, delete-orphan"
    )
