# app/services/printer/print_manager.py
from typing import Dict, Any, Optional
import win32print
import win32ui
from PIL import Image
import tempfile
import os
from fastapi import HTTPException
import asyncio
from concurrent.futures import ThreadPoolExecutor

class PrintManager:
    def __init__(self, printer_service: PrinterService, label_generator: LabelGenerator):
        self.printer_service = printer_service
        self.label_generator = label_generator
        self.print_queue = asyncio.Queue()
        self.executor = ThreadPoolExecutor(max_workers=2)
        
    async def start_print_queue(self):
        """Start processing print queue"""
        while True:
            print_job = await self.print_queue.get()
            try:
                await self.process_print_job(print_job)
            except Exception as e:
                print(f"Error processing print job: {str(e)}")
            finally:
                self.print_queue.task_done()
                
    async def process_print_job(self, print_job: Dict[str, Any]):
        """Process a print job"""
        job_type = print_job['type']
        data = print_job['data']
        printer = print_job.get('printer', self.printer_service.default_printer)
        
        if job_type == 'device':
            image = self.label_generator.create_device_label(data)
        elif job_type == 'export_box':
            image = self.label_generator.create_export_box_label(data)
        elif job_type == 'master_box':
            image = self.label_generator.create_master_box_label(data)
        else:
            raise ValueError(f"Unknown job type: {job_type}")
            
        await self.print_image(image, printer)
        
    async def print_image(self, image: Image, printer: str):
        """Print an image to specified printer"""
        def print_task():
            with tempfile.NamedTemporaryFile(delete=False, suffix='.bmp') as tmp:
                image.save(tmp.name, 'BMP')
                
            try:
                hprinter = win32print.OpenPrinter(printer)
                try:
                    win32print.StartDocPrinter(hprinter, 1, ("Label", None, "RAW"))
                    try:
                        win32print.StartPagePrinter(hprinter)
                        win32print.WritePrinter(hprinter, open(tmp.name, 'rb').read())
                        win32print.EndPagePrinter(hprinter)
                    finally:
                        win32print.EndDocPrinter(hprinter)
                finally:
                    win32print.ClosePrinter(hprinter)
            finally:
                os.unlink(tmp.name)
                
        await asyncio.get_event_loop().run_in_executor(self.executor, print_task)
        
    async def add_print_job(self, job_type: str, data: Dict[str, Any], 
                           printer: Optional[str] = None):
        """Add a print job to the queue"""
        await self.print_queue.put({
            'type': job_type,
            'data': data,
            'printer': printer
        })

