from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.application.use_cases import ClienteService
from src.application.dtos import ClienteCreate, ClienteUpdate, ClienteResponse
from src.presentation.api.dependencies import get_current_user

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post(
    "/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED
)
async def create_cliente(
    cliente_data: ClienteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new cliente."""
    try:
        cliente_service = ClienteService(db)
        return cliente_service.create_cliente(cliente_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ClienteResponse])
async def get_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all clientes."""
    cliente_service = ClienteService(db)
    return cliente_service.get_all_clientes(skip, limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get a cliente by ID."""
    try:
        cliente_service = ClienteService(db)
        return cliente_service.get_cliente(cliente_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def update_cliente(
    cliente_id: int,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Update a cliente."""
    try:
        cliente_service = ClienteService(db)
        return cliente_service.update_cliente(cliente_id, cliente_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a cliente."""
    try:
        cliente_service = ClienteService(db)
        cliente_service.delete_cliente(cliente_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
