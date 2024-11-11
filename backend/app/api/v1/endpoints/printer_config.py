# app/api/v1/endpoints/printer_config.py
from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from app.core.config import get_settings
from app.services.printer import LabelPrinter
from app.config.printer_config import PRINTER_CONFIG

router = APIRouter()

@router.get("/config")
def get_printer_config() -> Dict[str, Any]:
    """Get current printer configuration"""
    return PRINTER_CONFIG

@router.put("/config/default-printer")
def set_default_printer(printer_name: str) -> Dict[str, str]:
    """Set default printer"""
    if printer_name not in win32print.EnumPrinters(2):
        raise HTTPException(
            status_code=400,
            detail=f"Printer {printer_name} not found"
        )
    
    PRINTER_CONFIG['default_printer'] = printer_name
    return {"message": f"Default printer set to {printer_name}"}

@router.put("/config/label/{label_type}")
def update_label_config(
    label_type: str,
    config: Dict[str, Any]
) -> Dict[str, str]:
    """Update label configuration"""
    if label_type not in PRINTER_CONFIG['label_configs']:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown label type: {label_type}"
        )
    
    PRINTER_CONFIG['label_configs'][label_type].update(config)
    return {"message": f"Configuration updated for {label_type}"}
