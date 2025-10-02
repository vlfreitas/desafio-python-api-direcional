from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.application.use_cases import VendaService
from src.application.dtos import VendaCreate, VendaResponse
from src.presentation.api.dependencies import get_current_user

router = APIRouter(prefix="/vendas", tags=["Vendas"])


@router.post("/", response_model=VendaResponse, status_code=status.HTTP_201_CREATED)
async def create_venda(
    venda_data: VendaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new venda."""
    try:
        venda_service = VendaService(db)
        return venda_service.create_venda(venda_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[VendaResponse])
async def get_vendas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all vendas."""
    venda_service = VendaService(db)
    return venda_service.get_all_vendas(skip, limit)


@router.get("/{venda_id}", response_model=VendaResponse)
async def get_venda(
    venda_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get a venda by ID."""
    try:
        venda_service = VendaService(db)
        return venda_service.get_venda(venda_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{venda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_venda(
    venda_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a venda."""
    try:
        venda_service = VendaService(db)
        venda_service.delete_venda(venda_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
