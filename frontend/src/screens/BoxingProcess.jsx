// src/screens/BoxingProcess.jsx
import React, { useState } from 'react';
import { toast } from 'react-toastify';
import { QrScanner } from '../components/QrScanner';

const BoxingProcess = () => {
  const [currentBox, setCurrentBox] = useState(null);
  const [scannedDevices, setScannedDevices] = useState([]);

  const handleDeviceScan = async (qrData) => {
    if (!currentBox) {
      toast.error('Debe crear una caja primero');
      return;
    }

    try {
      const response = await fetch(`/api/v1/cajas/expositoras/${currentBox.id}/dispositivos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          qr_code: qrData,
          operario_id: localStorage.getItem('operarioId'),
        }),
      });

      if (response.ok) {
        const device = await response.json();
        setScannedDevices(prev => [...prev, device]);
        
        if (scannedDevices.length + 1 >= 24) {
          await completeBox();
        }
      }
    } catch (error) {
      toast.error('Error al registrar dispositivo en la caja');
    }
  };

  const createNewBox = async () => {
    try {
      const response = await fetch('/api/v1/cajas/expositoras', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          operario_id: localStorage.getItem('operarioId'),
          orden_produccion_id: currentOrderId, // Debe venir de algún estado global o contexto
        }),
      });

      if (response.ok) {
        const box = await response.json();
        setCurrentBox(box);
        setScannedDevices([]);
      }
    } catch (error) {
      toast.error('Error al crear nueva caja');
    }
  };

  const completeBox = async () => {
    try {
      const response = await fetch(`/api/v1/cajas/expositoras/${currentBox.id}/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        toast.success('Caja completada correctamente');
        setCurrentBox(null);
        setScannedDevices([]);
      }
    } catch (error) {
      toast.error('Error al completar la caja');
    }
  };

  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="space-y-4">
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-lg font-bold mb-4">Caja Actual</h2>
          {currentBox ? (
            <div className="space-y-2">
              <p><span className="font-medium">Código:</span> {currentBox.codigo_caja}</p>
              <p><span className="font-medium">Dispositivos:</span> {scannedDevices.length}/24</p>
              {scannedDevices.length >= 24 ? (
                <button
                  onClick={completeBox}
                  className="w-full bg-green-500 text-white p-2 rounded"
                >
                  Completar Caja
                </button>
              ) : (
                <QrScanner onScan={handleDeviceScan} />
              )}
            </div>
          ) : (
            <button
              onClick={createNewBox}
              className="w-full bg-blue-500 text-white p-2 rounded"
            >
              Crear Nueva Caja
            </button>
          )}
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow p-4">
        <h2 className="text-lg font-bold mb-4">Dispositivos Escaneados</h2>
        <div className="h-96 overflow-auto">
          <table className="min-w-full">
            <thead>
              <tr>
                <th className="px-4 py-2">Posición</th>
                <th className="px-4 py-2">IMEI</th>
                <th className="px-4 py-2">ICCID</th>
              </tr>
            </thead>
            <tbody>
              {scannedDevices.map((device, index) => (
                <tr key={index} className="border-t">
                  <td className="px-4 py-2">{index + 1}</td>
                  <td className="px-4 py-2">{device.imei}</td>
                  <td className="px-4 py-2">{device.iccid}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
