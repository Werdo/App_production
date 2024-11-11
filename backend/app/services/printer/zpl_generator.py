# app/services/printer/zpl_generator.py
from typing import Dict, Any
from string import Template
import os

class ZPLGenerator:
    def __init__(self, template_dir: str = "zpl_templates"):
        self.template_dir = template_dir

    def load_template(self, template_name: str) -> str:
        """Load ZPL template file"""
        template_path = os.path.join(self.template_dir, template_name)
        with open(template_path, 'r') as file:
            return file.read()

    def generate_device_label_zpl(self, data: Dict[str, Any]) -> str:
        """Generate ZPL for device label"""
        template = Template(self.load_template('device_label.zpl'))
        return template.substitute(
            imei=data['imei'],
            iccid=data['iccid'],
            imei_barcode=data['imei'],  # The printer will generate the barcode
            iccid_barcode=data['iccid']  # The printer will generate the barcode
        )

    def generate_export_box_zpl(self, data: Dict[str, Any]) -> str:
        """Generate ZPL for export box label"""
        template = Template(self.load_template('export_box_label.zpl'))
        
        # Format device list
        device_list = ""
        for i, device in enumerate(data['dispositivos'], 1):
            device_list += f"^FO50,{150 + i*30}^A0N,20,20^FD{i}. {device['imei']}^FS\n"
        
        return template.substitute(
            codigo_caja=data['codigo_caja'],
            orden_produccion=data['orden_produccion'],
            fecha=data['fecha'],
            qr_data=data['qr_data'],
            device_list=device_list
        )
