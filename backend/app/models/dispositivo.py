# app/models/dispositivo.py
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id = Column(Integer, primary_key=True, index=True)
    imei = Column(String(15), unique=True, index=True)
    iccid = Column(String(20), unique=True, index=True)
    orden_produccion_id = Column(Integer, ForeignKey("ordenes_produccion.id"))
    operario_id = Column(Integer, ForeignKey("operarios.id"))
    version_producto_id = Column(Integer, ForeignKey("versiones_producto.id"))
    lote_id = Column(Integer, ForeignKey("lotes_produccion.id"))
    es_oem = Column(Boolean, default=False)
    control_activo = Column(Boolean, default=True)
    bloqueado = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    orden_produccion = relationship("OrdenProduccion", back_populates="dispositivos")
    operario = relationship("Operario", back_populates="dispositivos")
    version_producto = relationship("VersionProducto", back_populates="dispositivos")
    lote = relationship("LoteProduccion", back_populates="dispositivos")
    registros_procesos = relationship("RegistroProceso", back_populates="dispositivo")
