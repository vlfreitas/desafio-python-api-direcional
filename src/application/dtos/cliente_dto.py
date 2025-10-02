from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ClienteBase(BaseModel):
    """Base Cliente schema."""

    nome: str = Field(..., min_length=1, max_length=255)
    cpf: str = Field(..., pattern=r"^\d{11}$")
    email: EmailStr
    telefone: str = Field(..., min_length=8, max_length=20)


class ClienteCreate(ClienteBase):
    """Schema for creating a cliente."""

    pass


class ClienteUpdate(BaseModel):
    """Schema for updating a cliente."""

    nome: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None
    telefone: str | None = Field(None, min_length=8, max_length=20)


class ClienteResponse(ClienteBase):
    """Schema for cliente response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
