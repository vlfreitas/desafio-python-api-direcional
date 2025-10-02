from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ReservaCreate(BaseModel):
    """Schema for creating a reserva."""

    cliente_id: int = Field(..., gt=0)
    apartamento_id: int = Field(..., gt=0)
    data_expiracao: datetime


class ReservaResponse(BaseModel):
    """Schema for reserva response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    apartamento_id: int
    data_reserva: datetime
    data_expiracao: datetime
    ativa: bool
    created_at: datetime
    updated_at: datetime
