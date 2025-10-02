from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class VendaCreate(BaseModel):
    """Schema for creating a venda."""

    cliente_id: int = Field(..., gt=0)
    apartamento_id: int = Field(..., gt=0)
    valor_venda: float = Field(..., gt=0)
    valor_entrada: float = Field(..., gt=0)


class VendaResponse(BaseModel):
    """Schema for venda response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    apartamento_id: int
    valor_venda: float
    valor_entrada: float
    data_venda: datetime
    created_at: datetime
    updated_at: datetime
