# app/services/printer/zpl_templates/device_label.zpl
^XA
^FO50,50^A0N,30,30^FDDevice Label^FS

^FO50,100^A0N,25,25^FDIMEI: ${imei}^FS
^FO50,150^BC,100,Y,N,N^FD${imei_barcode}^FS

^FO50,300^A0N,25,25^FDICCID: ${iccid}^FS
^FO50,350^BC,100,Y,N,N^FD${iccid_barcode}^FS

^XZ
