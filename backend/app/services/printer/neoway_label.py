# app/services/printer/neoway_label.py
from typing import Dict, Any
from datetime import datetime

class NeowayLabelGenerator:
    def __init__(self):
        """Initialize label generator for Neoway devices"""
        self.template = """
^XA

^FO50,50^A0N,40,40^FDneoway^FS

^FO50,100^A0N,25,25^FDProduct: ${product}^FS
^FO50,130^A0N,25,25^FDCaducidad: ${caducidad}^FS

^FO400,50^BQN,2,8^FDMM,A${qr_data}^FS

^FO50,180^BCN,80,Y,N,N^FD${imei}^FS
^FO50,270^A0N,20,20^FD${imei}^FS

^FO50,300^BCN,80,Y,N,N^FD${iccid}^FS
^FO50,390^A0N,20,20^FD${iccid}^FS

^FO50,430^A0N,25,25^FDMade in Spain^FS

^XZ
"""

    def generate_label_zpl(self, data: Dict[str, Any]) -> str:
        """
        Generate ZPL code for Neoway device label
        Elements:
        1. QR Code (top right)
        2. Product info (T912 V10)
        3. Caducidad (2038)
        4. IMEI barcode
        5. ICCID barcode
        6. Made in Spain text
        """
        from string import Template
        
        # Prepare QR data (can be customized based on requirements)
        qr_data = f"{data['imei']},{data['iccid']}"
        
        # Create template substitution
        label_data = {
            'product': data['product'],
            'caducidad': data['caducidad'],
            'qr_data': qr_data,
            'imei': data['imei'],
            'iccid': data['iccid']
        }
        
        return Template(self.template).substitute(label_data)

# app/services/printer/neoway_printer.py
class NeowayPrinter:
    def __init__(self, printer_config: Dict[str, Any]):
        self.config = printer_config
        self.label_generator = NeowayLabelGenerator()

    async def print_device_label(
        self,
        imei: str,
        iccid: str,
        product: str = "T912 V10",
        caducidad: str = "2038",
        printer_name: Optional[str] = None
    ) -> None:
        """Print Neoway device label"""
        try:
            zpl = self.label_generator.generate_label_zpl({
                'imei': imei,
                'iccid': iccid,
                'product': product,
                'caducidad': caducidad
            })
            
            printer = printer_name or self.config['default_printer']
            handle = win32print.OpenPrinter(printer)
            
            try:
                win32print.StartDocPrinter(handle, 1, ("Neoway Label", None, "RAW"))
                try:
                    win32print.StartPagePrinter(handle)
                    win32print.WritePrinter(handle, zpl.encode())
                    win32print.EndPagePrinter(handle)
                finally:
                    win32print.EndDocPrinter(handle)
            finally:
                win32print.ClosePrinter(handle)
                
        except Exception as e:
            raise Exception(f"Error printing Neoway label: {str(e)}")
