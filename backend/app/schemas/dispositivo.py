# app/schemas/dispositivo.py
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DispositivoBase(BaseModel):
    imei: Optional[str] = None
    iccid: Optional[str] = None
    orden_produccion_id: Optional[int] = None
    version_producto_id: Optional[int] = None
    es_oem: Optional[bool] = False

class DispositivoCreate(DispositivoBase):
    qr_code: str
    orden_produccion_id: int

class DispositivoUpdate(DispositivoBase):
    control_activo: Optional[bool] = None
    bloqueado: Optional[bool] = None

class DispositivoInDBBase(DispositivoBase):
    id: int
    operario_id: int
    created_at: datetime
    control_activo: bool
    bloqueado: bool

    class Config:
        from_attributes = True

class DispositivoInDB(DispositivoInDBBase):
    pass
