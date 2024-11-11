# app/config/printer_config.py
from typing import Dict, Any

PRINTER_CONFIG = {
    'default_printer': 'ZEBRA ZT411',
    'label_configs': {
        'device': {
            'width': 400,
            'height': 200,
            'dpi': 203,
            'margin': 10,
            'font_size': 20,
            'barcode_height': 50,
            'template': 'zpl_templates/device_label.zpl'
        },
        'export_box': {
            'width': 600,
            'height': 400,
            'dpi': 203,
            'margin': 15,
            'font_size': 24,
            'qr_size': 150,
            'template': 'zpl_templates/export_box_label.zpl'
        },
        'master_box': {
            'width': 800,
            'height': 600,
            'dpi': 203,
            'margin': 20,
            'font_size': 28,
            'qr_size': 200,
            'template': 'zpl_templates/master_box_label.zpl'
        }
    }
}
