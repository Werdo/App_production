# app/api/v1/endpoints/print.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.operario import Operario
from app.services.printer import PrintManager, PrinterService, LabelGenerator

router = APIRouter()

@router.get("/printers")
def get_printers() -> List[str]:
    """Get list of available printers"""
    printer_service = PrinterService(config={})  # Load config from settings
    return printer_service.get_available_printers()

@router.post("/print/device/{imei}")
async def print_device_label(
    *,
    db: Session = Depends(deps.get_db),
    imei: str,
    printer: Optional[str] = None,
    current_operario: Operario = Depends(deps.get_current_operario)
) -> Any:
    """Print device label"""
    dispositivo = db.query(models.Dispositivo).filter(
        models.Dispositivo.imei == imei
    ).first()
    
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Device not found")
        
    printer_service = PrinterService(config={})
    label_generator = LabelGenerator(printer_service)
    print_manager = PrintManager(printer_service, label_generator)
    
    await print_manager.add_print_job(
        'device',
        {
            'imei': dispositivo.imei,
            'iccid': dispositivo.iccid
        },
        printer
    )
    
    return {"message": "Print job added to queue"}

@router.post("/print/export-box/{box_id}")
async def print_export_box_label(
    *,
    db: Session = Depends(deps.get_db),
    box_id: int,
    printer: Optional[str] = None,
    current_operario: Operario = Depends(deps.get_current_operario)
) -> Any:
    """Print export box label"""
    box = db.query(models.CajaExpositora).filter(
        models.CajaExpositora.id == box_id
    ).first()
    
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")
        
    devices = db.query(models.Dispositivo).join(
        models.DispositivosCajaExpositora
    ).filter(
        models.DispositivosCajaExpositora.caja_expositora_id == box_id
    ).all()
    
    printer_service = PrinterService(config={})
    label_generator = LabelGenerator(printer_service)
    print_manager = PrintManager(printer_service, label_generator)
    
    await print_manager.add_print_job(
        'export_box',
        {
            'codigo_caja': box.codigo_caja,
            'orden_produccion': box.orden_produccion.numero_orden,
            'dispositivos': [{'imei': d.imei} for d in devices]
        },
        printer
    )
    
    return {"message": "Print job added to queue"}

@router.post("/print/master-box/{box_id}")
async def print_master_box_label(
    *,
    db: Session = Depends(deps.get_db),
    box_id: int,
    printer: Optional[str] = None,
    current_operario: Operario = Depends(deps.get_current_operario)
) -> Any:
    """Print master box label"""
    box = db.query(models.CajaMaster).filter(
        models.CajaMaster.id == box_id
    ).first()
    
    if not box:
        raise HTTPException(status_code=404, detail="Master box not found")
        
    export_boxes = db.query(models.CajaExpositora).join(
        models.ExpositorasCajaMaster
    ).filter(
        models.ExpositorasCajaMaster.caja_master_id == box_id
    ).all()
    
    printer_service = PrinterService(config={})
    label_generator = LabelGenerator(printer_service)
    print_manager = PrintManager(printer_service, label_generator)
    
    await print_manager.add_print_job(
        'master_box',
        {
            'codigo_caja': box.codigo_caja,
            'orden_produccion': box.orden_produccion.numero_orden,
            'cliente': box.orden_produccion.cliente,
            'cajas_expositoras': [{
                'codigo_caja': eb.codigo_caja
            } for eb in export_boxes]
        },
        printer
    )
    
    return {"message": "Print job added to queue"}


