from .auth import router as auth_router
from .clientes import router as clientes_router
from .apartamentos import router as apartamentos_router
from .vendas import router as vendas_router
from .reservas import router as reservas_router

__all__ = [
    "auth_router",
    "clientes_router",
    "apartamentos_router",
    "vendas_router",
    "reservas_router",
]
