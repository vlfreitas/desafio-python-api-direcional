from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.application.use_cases import ReservaService
from src.application.dtos import ReservaCreate, ReservaResponse
from src.presentation.api.dependencies import get_current_user

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
async def create_reserva(
    reserva_data: ReservaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new reserva."""
    try:
        reserva_service = ReservaService(db)
        return reserva_service.create_reserva(reserva_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ReservaResponse])
async def get_reservas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get all reservas."""
    reserva_service = ReservaService(db)
    return reserva_service.get_all_reservas(skip, limit)


@router.get("/{reserva_id}", response_model=ReservaResponse)
async def get_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get a reserva by ID."""
    try:
        reserva_service = ReservaService(db)
        return reserva_service.get_reserva(reserva_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{reserva_id}/cancel", response_model=dict)
async def cancel_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Cancel a reserva."""
    try:
        reserva_service = ReservaService(db)
        reserva_service.cancel_reserva(reserva_id)
        return {"message": "Reserva cancelled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a reserva."""
    try:
        reserva_service = ReservaService(db)
        reserva_service.delete_reserva(reserva_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
