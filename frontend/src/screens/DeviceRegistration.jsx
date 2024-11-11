// src/screens/DeviceRegistration.jsx
import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { QrScanner } from '../components/QrScanner';

const DeviceRegistration = () => {
  const [orderInfo, setOrderInfo] = useState(null);
  const [scannedDevices, setScannedDevices] = useState([]);
  const [scanning, setScanning] = useState(true);

  const handleDeviceScan = async (qrData) => {
    try {
      const response = await fetch('/api/v1/dispositivos/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          qr_code: qrData,
          orden_produccion_id: orderInfo.id,
          operario_id: localStorage.getItem('operarioId'),
          proceso_id: 1, // Ajustar según el proceso actual
        }),
      });

      if (response.ok) {
        const device = await response.json();
        setScannedDevices(prev => [...prev, device]);
        toast.success('Dispositivo registrado correctamente');
      }
    } catch (error) {
      toast.error('Error al registrar dispositivo');
    }
  };

  return (
    <div className="grid grid-cols-5 gap-4 h-full">
      {/* Panel de información (20%) */}
      <div className="col-span-1 bg-white rounded-lg shadow p-4">
        <h2 className="text-lg font-bold mb-4">Información de Producción</h2>
        {orderInfo && (
          <div className="space-y-2">
            <p><span className="font-medium">Orden:</span> {orderInfo.numero_orden}</p>
            <p><span className="font-medium">Modelo:</span> {orderInfo.modelo}</p>
            <p><span className="font-medium">Progreso:</span> {scannedDevices.length}/{orderInfo.cantidad_total}</p>
          </div>
        )}
      </div>

      {/* Área de trabajo (80%) */}
      <div className="col-span-4 bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-4">
            <h2 className="text-lg font-bold">Registro de Dispositivos</h2>
            {scanning && <QrScanner onScan={handleDeviceScan} />}
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">Últimos Registros</h3>
            <div className="h-96 overflow-auto">
              <table className="min-w-full">
                <thead>
                  <tr>
                    <th className="px-4 py-2">IMEI</th>
                    <th className="px-4 py-2">ICCID</th>
                    <th className="px-4 py-2">Hora</th>
                  </tr>
                </thead>
                <tbody>
                  {scannedDevices.map((device, index) => (
                    <tr key={index} className="border-t">
                      <td className="px-4 py-2">{device.imei}</td>
                      <td className="px-4 py-2">{device.iccid}</td>
                      <td className="px-4 py-2">
                        {new Date(device.created_at).toLocaleTimeString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
