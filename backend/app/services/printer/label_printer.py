# app/services/printer/label_printer.py
from typing import Dict, Any, Optional
import win32print
import asyncio
from .zpl_generator import ZPLGenerator

class LabelPrinter:
    def __init__(self, printer_config: Dict[str, Any]):
        self.config = printer_config
        self.zpl_generator = ZPLGenerator()
        self.print_queue = asyncio.Queue()

    async def print_label(
        self,
        label_type: str,
        data: Dict[str, Any],
        printer_name: Optional[str] = None
    ) -> None:
        """Send label to printer"""
        if label_type == 'device':
            zpl = self.zpl_generator.generate_device_label_zpl(data)
        elif label_type == 'export_box':
            zpl = self.zpl_generator.generate_export_box_zpl(data)
        elif label_type == 'master_box':
            zpl = self.zpl_generator.generate_master_box_zpl(data)
        else:
            raise ValueError(f"Unknown label type: {label_type}")

        printer = printer_name or self.config['default_printer']
        await self.send_to_printer(zpl, printer)

    async def send_to_printer(self, zpl: str, printer_name: str) -> None:
        """Send ZPL code to printer"""
        try:
            handle = win32print.OpenPrinter(printer_name)
            try:
                win32print.StartDocPrinter(handle, 1, ("Label", None, "RAW"))
                try:
                    win32print.StartPagePrinter(handle)
                    win32print.WritePrinter(handle, zpl.encode())
                    win32print.EndPagePrinter(handle)
                finally:
                    win32print.EndDocPrinter(handle)
            finally:
                win32print.ClosePrinter(handle)
        except Exception as e:
            raise Exception(f"Error printing to {printer_name}: {str(e)}")
