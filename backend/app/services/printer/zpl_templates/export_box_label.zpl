# app/services/printer/zpl_templates/export_box_label.zpl
^XA
^FO50,50^A0N,40,40^FDCaja Expositora^FS

^FO50,100^A0N,30,30^FDCódigo: ${codigo_caja}^FS
^FO50,150^A0N,30,30^FDOrden: ${orden_produccion}^FS
^FO50,200^A0N,30,30^FDFecha: ${fecha}^FS

^FO400,50^BQN,2,10^FD${qr_data}^FS

${device_list}

^XZ
