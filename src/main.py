from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.api.routes import (
    auth_router,
    clientes_router,
    apartamentos_router,
    vendas_router,
    reservas_router,
)

app = FastAPI(
    title="Direcional API",
    description="API for managing real estate sales",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(clientes_router)
app.include_router(apartamentos_router)
app.include_router(vendas_router)
app.include_router(reservas_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Direcional API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
