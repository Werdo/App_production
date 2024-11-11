// src/components/QrScanner.jsx
import React from 'react';
import { Html5QrcodeScanner } from 'html5-qrcode';

export const QrScanner = ({ onScan }) => {
  React.useEffect(() => {
    const scanner = new Html5QrcodeScanner('reader', {
      qrbox: {
        width: 250,
        height: 250,
      },
      fps: 5,
    });

    scanner.render(
      (data) => {
        scanner.clear();
        onScan(data);
      },
      (error) => {
        console.warn(error);
      }
    );

    return () => {
      scanner.clear();
    };
  }, [onScan]);

  return <div id="reader" />;
};
