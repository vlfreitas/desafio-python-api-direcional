from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.application.use_cases import ApartamentoService
from src.application.dtos import ApartamentoCreate, ApartamentoUpdate, ApartamentoResponse
from src.infrastructure.database.models.apartamento import StatusApartamento
from src.presentation.api.dependencies import get_current_user

router = APIRouter(prefix="/apartamentos", tags=["Apartamentos"])


@router.post(
    "/", response_model=ApartamentoResponse, status_code=status.HTTP_201_CREATED
)
async def create_apartamento(
    apartamento_data: ApartamentoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new apartamento."""
    try:
        apartamento_service = ApartamentoService(db)
        return apartamento_service.create_apartamento(apartamento_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ApartamentoResponse])
async def get_apartamentos(
    skip: int = 0,
    limit: int = 100,
    status: StatusApartamento | None = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all apartamentos, optionally filtered by status."""
    apartamento_service = ApartamentoService(db)
    if status:
        return apartamento_service.get_apartamentos_by_status(status, skip, limit)
    return apartamento_service.get_all_apartamentos(skip, limit)


@router.get("/{apartamento_id}", response_model=ApartamentoResponse)
async def get_apartamento(
    apartamento_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get an apartamento by ID."""
    try:
        apartamento_service = ApartamentoService(db)
        return apartamento_service.get_apartamento(apartamento_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{apartamento_id}/disponibilidade")
async def check_disponibilidade(
    apartamento_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Check if apartamento is available."""
    try:
        apartamento_service = ApartamentoService(db)
        disponivel = apartamento_service.check_disponibilidade(apartamento_id)
        return {"apartamento_id": apartamento_id, "disponivel": disponivel}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{apartamento_id}", response_model=ApartamentoResponse)
async def update_apartamento(
    apartamento_id: int,
    apartamento_data: ApartamentoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Update an apartamento."""
    try:
        apartamento_service = ApartamentoService(db)
        return apartamento_service.update_apartamento(apartamento_id, apartamento_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{apartamento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_apartamento(
    apartamento_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete an apartamento."""
    try:
        apartamento_service = ApartamentoService(db)
        apartamento_service.delete_apartamento(apartamento_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
