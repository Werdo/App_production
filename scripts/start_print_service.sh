#!/bin/bash
# Iniciar CUPS
service cups start

# Configurar impresora si está definida
if [ ! -z "$PRINTER_NAME" ]; then
    # Esperar a que CUPS esté listo
    until lpstat -r; do
        echo "Waiting for CUPS..."
        sleep 1
    done

    # Añadir impresora
    lpadmin -p $PRINTER_NAME -E -v socket://$PRINTER_IP:9100 -m raw
    cupsenable $PRINTER_NAME
    cupsaccept $PRINTER_NAME
fi

# Iniciar el servicio de impresión
python3 print_service.py
