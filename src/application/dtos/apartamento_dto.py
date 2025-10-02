from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from src.infrastructure.database.models.apartamento import StatusApartamento


class ApartamentoBase(BaseModel):
    """Base Apartamento schema."""

    numero: str = Field(..., min_length=1, max_length=10)
    bloco: str = Field(..., min_length=1, max_length=10)
    andar: int = Field(..., ge=0)
    quartos: int = Field(..., ge=1)
    area: float = Field(..., gt=0)
    preco: float = Field(..., gt=0)


class ApartamentoCreate(ApartamentoBase):
    """Schema for creating an apartamento."""

    pass


class ApartamentoUpdate(BaseModel):
    """Schema for updating an apartamento."""

    numero: str | None = Field(None, min_length=1, max_length=10)
    bloco: str | None = Field(None, min_length=1, max_length=10)
    andar: int | None = Field(None, ge=0)
    quartos: int | None = Field(None, ge=1)
    area: float | None = Field(None, gt=0)
    preco: float | None = Field(None, gt=0)
    status: StatusApartamento | None = None


class ApartamentoResponse(ApartamentoBase):
    """Schema for apartamento response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    status: StatusApartamento
    created_at: datetime
    updated_at: datetime
