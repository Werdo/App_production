// src/components/Header.jsx
import React from 'react';
import { Clock } from 'lucide-react';

export const Header = () => {
  const [time, setTime] = React.useState(new Date());

  React.useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="bg-white border-b border-gray-200 p-4">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold">Sistema de Producción</h1>
        <div className="flex items-center gap-2">
          <Clock className="w-5 h-5" />
          <span className="font-mono">
            {time.toLocaleTimeString()}
          </span>
        </div>
      </div>
    </header>
  );
};
