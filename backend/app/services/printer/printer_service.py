# app/services/printer/printer_service.py
from typing import List, Optional, Dict, Any
import win32print
import win32ui
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
import json
from datetime import datetime
from fastapi import HTTPException

class PrinterService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.default_printer = config.get('default_printer')
        self.label_configs = config.get('label_configs', {})
        
    def get_available_printers(self) -> List[str]:
        """Get list of available printers"""
        printers = []
        for printer in win32print.EnumPrinters(2):
            printers.append(printer[2])
        return printers
    
    def set_default_printer(self, printer_name: str) -> None:
        """Set default printer for labels"""
        if printer_name not in self.get_available_printers():
            raise HTTPException(
                status_code=400,
                detail=f"Printer {printer_name} not found"
            )
        self.default_printer = printer_name
        
    def generate_barcode(self, data: str, barcode_type: str = 'code128') -> Image:
        """Generate barcode image"""
        barcode_class = barcode.get_barcode_class(barcode_type)
        rv = BytesIO()
        barcode_class(data, writer=ImageWriter()).write(rv)
        image = Image.open(rv)
        return image
    
    def generate_qr(self, data: str) -> Image:
        """Generate QR code image"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")

class LabelGenerator:
    def __init__(self, printer_service: PrinterService):
        self.printer_service = printer_service
        self.font = ImageFont.truetype("arial.ttf", 20)
        
    def create_device_label(self, device_data: Dict[str, Any]) -> Image:
        """Create label for individual device"""
        # Get label configuration
        config = self.printer_service.label_configs.get('device', {})
        width = config.get('width', 400)
        height = config.get('height', 200)
        
        # Create base image
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Add IMEI barcode
        imei_barcode = self.printer_service.generate_barcode(device_data['imei'])
        image.paste(imei_barcode, (20, 20))
        draw.text((20, 70), f"IMEI: {device_data['imei']}", fill='black', font=self.font)
        
        # Add ICCID barcode
        iccid_barcode = self.printer_service.generate_barcode(device_data['iccid'])
        image.paste(iccid_barcode, (20, 100))
        draw.text((20, 150), f"ICCID: {device_data['iccid']}", fill='black', font=self.font)
        
        return image
    
    def create_export_box_label(self, box_data: Dict[str, Any]) -> Image:
        """Create label for export box"""
        config = self.printer_service.label_configs.get('export_box', {})
        width = config.get('width', 600)
        height = config.get('height', 400)
        
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Add box information
        draw.text((20, 20), f"Caja Expositora: {box_data['codigo_caja']}", 
                 fill='black', font=self.font)
        draw.text((20, 50), f"Orden: {box_data['orden_produccion']}", 
                 fill='black', font=self.font)
        draw.text((20, 80), f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", 
                 fill='black', font=self.font)
        
        # Add QR code with box data
        qr_data = {
            'tipo': 'EXPOSITORA',
            'codigo': box_data['codigo_caja'],
            'orden': box_data['orden_produccion'],
            'dispositivos': [d['imei'] for d in box_data['dispositivos']]
        }
        qr_image = self.printer_service.generate_qr(json.dumps(qr_data))
        image.paste(qr_image, (400, 20))
        
        # Add device list
        y_pos = 120
        for i, device in enumerate(box_data['dispositivos'], 1):
            draw.text((20, y_pos), f"{i}. IMEI: {device['imei']}", 
                     fill='black', font=self.font)
            y_pos += 25
            
        return image
    
    def create_master_box_label(self, master_box_data: Dict[str, Any]) -> Image:
        """Create label for master box"""
        config = self.printer_service.label_configs.get('master_box', {})
        width = config.get('width', 800)
        height = config.get('height', 600)
        
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Add master box information
        draw.text((20, 20), f"Caja Master: {master_box_data['codigo_caja']}", 
                 fill='black', font=self.font)
        draw.text((20, 50), f"Orden: {master_box_data['orden_produccion']}", 
                 fill='black', font=self.font)
        draw.text((20, 80), f"Cliente: {master_box_data['cliente']}", 
                 fill='black', font=self.font)
        draw.text((20, 110), f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", 
                 fill='black', font=self.font)
        
        # Add QR code with master box data
        qr_data = {
            'tipo': 'MASTER',
            'codigo': master_box_data['codigo_caja'],
            'orden': master_box_data['orden_produccion'],
            'cajas_expositoras': [c['codigo_caja'] for c in master_box_data['cajas_expositoras']]
        }
        qr_image = self.printer_service.generate_qr(json.dumps(qr_data))
        image.paste(qr_image, (600, 20))
        
        # Add export box list
        y_pos = 150
        for i, box in enumerate(master_box_data['cajas_expositoras'], 1):
            draw.text((20, y_pos), f"Caja Expositora {i}: {box['codigo_caja']}", 
                     fill='black', font=self.font)
            y_pos += 30
            
        return image
