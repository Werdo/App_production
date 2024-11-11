# app/schemas/caja.py
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class CajaExpositoraBase(BaseModel):
    orden_produccion_id: int
    operario_id: int

class CajaExpositoraCreate(CajaExpositoraBase):
    pass

class CajaExpositoraUpdate(CajaExpositoraBase):
    estado: Optional[str] = None

class CajaExpositoraInDB(CajaExpositoraBase):
    id: int
    codigo_caja: str
    estado: str
    cantidad_dispositivos: int
    created_at: datetime

    class Config:
        from_attributes = True

class CajaMasterBase(BaseModel):
    orden_produccion_id: int
    operario_id: int

class CajaMasterCreate(CajaMasterBase):
    cajas_expositoras: List[int]  # Lista de IDs de cajas expositoras

class CajaMasterInDB(CajaMasterBase):
    id: int
    codigo_caja: str
    estado: str
    cantidad_expositoras: int
    created_at: datetime

    class Config:
        from_attributes = True
