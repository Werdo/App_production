# app/api/v1/endpoints/dispositivos.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.dispositivo import (
    DispositivoCreate,
    DispositivoUpdate,
    DispositivoInDB
)
from app.models.operario import Operario
from app.services.dispositivo import DispositivoService

router = APIRouter()

@router.post("/", response_model=DispositivoInDB)
def create_dispositivo(
    *,
    db: Session = Depends(deps.get_db),
    dispositivo_in: DispositivoCreate,
    current_operario: Operario = Depends(deps.get_current_operario)
) -> Any:
    """
    Create new device.
    """
    service = DispositivoService(db)
    return service.create(dispositivo_in, current_operario)

@router.get("/{imei}", response_model=DispositivoInDB)
def read_dispositivo(
    *,
    db: Session = Depends(deps.get_db),
    imei: str,
) -> Any:
    """
    Get device by IMEI.
    """
    service = DispositivoService(db)
    dispositivo = service.get_by_imei(imei)
    if not dispositivo:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )
    return dispositivo

@router.put("/{imei}", response_model=DispositivoInDB)
def update_dispositivo(
    *,
    db: Session = Depends(deps.get_db),
    imei: str,
    dispositivo_in: DispositivoUpdate,
    current_operario: Operario = Depends(deps.get_current_operario)
) -> Any:
    """
    Update device.
    """
    service = DispositivoService(db)
    dispositivo = service.get_by_imei(imei)
    if not dispositivo:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )
    return service.update(dispositivo, dispositivo_in)
