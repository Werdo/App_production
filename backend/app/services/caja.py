# app/services/caja.py
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.caja import CajaExpositora, CajaMaster
from app.models.dispositivo import Dispositivo
from app.schemas.caja import CajaExpositoraCreate, CajaMasterCreate
import datetime

class CajaService:
    def __init__(self, db: Session):
        self.db = db

    def generate_box_code(self, prefix: str, order_id: int) -> str:
        """Generate unique box code"""
        date_str = datetime.datetime.now().strftime("%y%m%d")
        count = self.db.query(CajaExpositora).filter(
            CajaExpositora.codigo_caja.like(f"{prefix}{date_str}%")
        ).count()
        return f"{prefix}{date_str}{str(count + 1).zfill(4)}"

    def create_caja_expositora(
        self, caja_in: CajaExpositoraCreate
    ) -> CajaExpositora:
        """Create new export box"""
        codigo = self.generate_box_code("EXP", caja_in.orden_produccion_id)
        
        caja = CajaExpositora(
            codigo_caja=codigo,
            orden_produccion_id=caja_in.orden_produccion_id,
            operario_id=caja_in.operario_id,
            estado="EN_PROCESO"
        )
        
        try:
            self.db.add(caja)
            self.db.commit()
            self.db.refresh(caja)
            return caja
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error creating export box: {str(e)}"
            )

    def add_device_to_box(
        self,
        caja_id: int,
        imei: str,
        operario_id: int
    ) -> Dispositivo:
        """Add device to export box"""
        caja = self.db.query(CajaExpositora).filter(
            CajaExpositora.id == caja_id
        ).first()
        
        if not caja:
            raise HTTPException(
                status_code=404,
                detail="Export box not found"
            )
            
        if caja.estado != "EN_PROCESO":
            raise HTTPException(
                status_code=400,
                detail="Box is not in process"
            )
            
        if caja.cantidad_dispositivos >= 24:
            raise HTTPException(
                status_code=400,
                detail="Box is full"
            )

        dispositivo = self.db.query(Dispositivo).filter(
            Dispositivo.imei == imei
        ).first()
        
        if not dispositivo:
            raise HTTPException(
                status_code=404,
                detail="Device not found"
            )
            
        try:
            caja.dispositivos.append(dispositivo)
            caja.cantidad_dispositivos += 1
            self.db.commit()
            self.db.refresh(caja)
            return dispositivo
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error adding device to box: {str(e)}"
            )

    def complete_caja_expositora(self, caja_id: int) -> CajaExpositora:
        """Complete export box"""
        caja = self.db.query(CajaExpositora).filter(
            CajaExpositora.id == caja_id
        ).first()
        
        if not caja:
            raise HTTPException(
                status_code=404,
                detail="Export box not found"
            )
            
        if caja.cantidad_dispositivos != 24:
            raise HTTPException(
                status_code=400,
                detail="Box must have exactly 24 devices"
            )
            
        try:
            caja.estado = "COMPLETA"
            self.db.commit()
            self.db.refresh(caja)
            return caja
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error completing box: {str(e)}"
            )

    def create_caja_master(
        self, caja_in: CajaMasterCreate
    ) -> CajaMaster:
        """Create new master box"""
        if len(caja_in.cajas_expositoras) != 4:
            raise HTTPException(
                status_code=400,
                detail="Master box must have exactly 4 export boxes"
            )
            
        codigo = self.generate_box_code("MST", caja_in.orden_produccion_id)
        
        caja_master = CajaMaster(
            codigo_caja=codigo,
            orden_produccion_id=caja_in.orden_produccion_id,
            operario_id=caja_in.operario_id,
            estado="EN_PROCESO"
        )
        
        try:
            self.db.add(caja_master)
            self.db.flush()
            
            # Add export boxes
            for caja_exp_id in caja_in.cajas_expositoras:
                caja_exp = self.db.query(CajaExpositora).filter(
                    CajaExpositora.id == caja_exp_id,
                    CajaExpositora.estado == "COMPLETA"
                ).first()
                
                if not caja_exp:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Export box {caja_exp_id} not found or not complete"
                    )
                
                caja_master.cajas_expositoras.append(caja_exp)
                caja_exp.estado = "ASIGNADA"
            
            caja_master.cantidad_expositoras = 4
            caja_master.estado = "COMPLETA"
            
            self.db.commit()
            self.db.refresh(caja_master)
            return caja_master
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error creating master box: {str(e)}"
            )
