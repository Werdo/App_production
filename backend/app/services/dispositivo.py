# app/services/dispositivo.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.dispositivo import Dispositivo
from app.models.operario import Operario
from app.schemas.dispositivo import DispositivoCreate, DispositivoUpdate
from fastapi import HTTPException

class DispositivoService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_imei(self, imei: str) -> Optional[Dispositivo]:
        return self.db.query(Dispositivo).filter(Dispositivo.imei == imei).first()

    def parse_qr_code(self, qr_code: str) -> tuple[str, str]:
        """Parse QR code to extract IMEI and ICCID"""
        try:
            imei, iccid = qr_code.strip().split()
            if len(imei) != 15:
                raise ValueError("IMEI must be 15 characters")
            if not iccid:
                raise ValueError("ICCID is required")
            return imei, iccid
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid QR code format: {str(e)}"
            )

    def create(self, dispositivo_in: DispositivoCreate, operario: Operario) -> Dispositivo:
        """Create new device from QR code"""
        imei, iccid = self.parse_qr_code(dispositivo_in.qr_code)
        
        # Check if device already exists
        if self.get_by_imei(imei):
            raise HTTPException(
                status_code=400,
                detail="Device with this IMEI already exists"
            )
        
        # Create device
        dispositivo = Dispositivo(
            imei=imei,
            iccid=iccid,
            orden_produccion_id=dispositivo_in.orden_produccion_id,
            operario_id=operario.id,
            version_producto_id=dispositivo_in.version_producto_id,
            es_oem=dispositivo_in.es_oem
        )
        
        try:
            self.db.add(dispositivo)
            self.db.commit()
            self.db.refresh(dispositivo)
            return dispositivo
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error creating device: {str(e)}"
            )

    def update(self, dispositivo: Dispositivo, dispositivo_in: DispositivoUpdate) -> Dispositivo:
        """Update device attributes"""
        for field, value in dispositivo_in.dict(exclude_unset=True).items():
            setattr(dispositivo, field, value)
        
        try:
            self.db.commit()
            self.db.refresh(dispositivo)
            return dispositivo
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error updating device: {str(e)}"
            )
