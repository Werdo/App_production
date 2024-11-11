# app/api/v1/endpoints/neoway_print.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.printer.neoway_printer import NeowayPrinter
from app.config.printer_config import PRINTER_CONFIG
from typing import Optional

router = APIRouter()

@router.post("/print/neoway-device")
async def print_neoway_label(
    imei: str,
    iccid: str,
    product: Optional[str] = "T912 V10",
    caducidad: Optional[str] = "2038",
    printer: Optional[str] = None
) -> Dict[str, str]:
    """
    Print Neoway device label
    """
    try:
        printer_service = NeowayPrinter(PRINTER_CONFIG)
        await printer_service.print_device_label(
            imei=imei,
            iccid=iccid,
            product=product,
            caducidad=caducidad,
            printer_name=printer
        )
        return {"message": "Label printed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error printing label: {str(e)}"
        )

# Configuración específica para etiquetas Neoway
NEOWAY_LABEL_CONFIG = {
    'dimensions': {
        'width': 100,  # mm
        'height': 50,  # mm
    },
    'elements': {
        'qr_code': {
            'position': {'x': 400, 'y': 50},
            'size': 8
        },
        'product_info': {
            'position': {'x': 50, 'y': 100},
            'font_size': 25
        },
        'barcodes': {
            'height': 80,
            'spacing': 90
        },
        'text': {
            'font': 'Arial',
            'size': {
                'brand': 40,
                'info': 25,
                'codes': 20
            }
        }
    }
}
