// src/screens/LoginScreen.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { QrScanner } from '../components/QrScanner';

const LoginScreen = () => {
  const navigate = useNavigate();
  const [scanning, setScanning] = useState(false);

  const handleScan = async (data) => {
    if (data) {
      try {
        const response = await fetch('/api/v1/operarios/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ qr_code: data }),
        });

        if (response.ok) {
          const operario = await response.json();
          localStorage.setItem('operarioId', operario.id);
          localStorage.setItem('operarioNombre', operario.nombre);
          navigate('/dashboard');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full">
        <h2 className="text-2xl font-bold text-center mb-6">
          Iniciar Sesión
        </h2>
        {scanning ? (
          <div className="space-y-4">
            <QrScanner onScan={handleScan} />
            <button
              onClick={() => setScanning(false)}
              className="w-full bg-gray-500 text-white p-2 rounded"
            >
              Cancelar
            </button>
          </div>
        ) : (
          <button
            onClick={() => setScanning(true)}
            className="w-full bg-blue-500 text-white p-2 rounded"
          >
            Escanear Código QR
          </button>
        )}
      </div>
    </div>
  );
};
