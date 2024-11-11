# app/api/v1/endpoints/cajas.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.caja import (
    CajaExpositoraCreate,
    CajaExpositoraInDB,
    CajaMasterCreate,
    CajaMasterInDB
)
from app.models.operario import Operario
from app.services.caja import CajaService

router = APIRouter()

@router.post("/expositoras/", response_model=CajaExpositoraInDB)
def create_caja_expositora(
    *,
    db: Session = Depends(deps.get_db),
    caja_in: CajaExpositoraCreate,
    current_operario: Operario = Depends(deps.get_current_operario)
) -> Any:
    """
    Create new export box.
    """
    service = CajaService(db)
    return service.create_caja_expositora(caja_in)

@router.post("/expositoras/{caja_id}/dispositivos")
def add_device_to_box(
    *,
    db: Session = Depends(deps.get_db),
    caja_id: int,
    imei: str,
    current_operario: Operario = Depends(deps.get_current_operario)
) -> Any:
    """
    Add device to export box.
    """
    service = CajaService(db)
    return service.add_device_to_box(caja_id, imei, current_operario.id)

@router.post("/expositoras/{caja_id}/complete", response_model=CajaExpositoraInDB)
def complete_caja_expositora(
    *,
    db: Session = Depends(deps.get_db),
    caja_id: int,
    current_operario: Operario = Depends(deps.get_current_operario)
) -> Any:
    """
    Complete export box.
    """
    service = CajaService(db)
    return service.complete_caja_expositora(caja_id)

@router.post("/master/", response_model=CajaMasterInDB)
def create_caja_master(
    *,
    db: Session = Depends(deps.get_db),
    caja_in: CajaMasterCreate,
    current_operario: Operario = Depends(deps.get_current_operario)
) -> Any:
    """
    Create new master box.
    """
    service = CajaService(db)
    return service.create_caja_master(caja_in)

@router.get("/expositoras/{caja_id}", response_model=CajaExpositoraInDB)
def get_caja_expositora(
    *,
    db: Session = Depends(deps.get_db),
    caja_id: int,
) -> Any:
    """
    Get export box by ID.
    """
    caja = db.query(CajaExpositora).filter(
        CajaExpositora.id == caja_id
    ).first()
    if not caja:
        raise HTTPException(
            status_code=404,
            detail="Export box not found"
        )
    return caja

@router.get("/master/{caja_id}", response_model=CajaMasterInDB)
def get_caja_master(
    *,
    db: Session = Depends(deps.get_db),
    caja_id: int,
) -> Any:
    """
    Get master box by ID.
    """
    caja = db.query(CajaMaster).filter(
        CajaMaster.id == caja_id
    ).first()
    if not caja:
        raise HTTPException(
            status_code=404,
            detail="Master box not found"
        )
    return caja
