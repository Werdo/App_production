// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import LoginScreen from './screens/LoginScreen';
import ProductionDashboard from './screens/ProductionDashboard';
import DeviceRegistration from './screens/DeviceRegistration';
import BoxingProcess from './screens/BoxingProcess';
import MasterBoxing from './screens/MasterBoxing';
import ReportsScreen from './screens/ReportsScreen';

import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const App = () => {
  return (
    <BrowserRouter>
      <ToastContainer position="top-right" />
      <Routes>
        <Route path="/" element={<LoginScreen />} />
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<ProductionDashboard />} />
          <Route path="/register" element={<DeviceRegistration />} />
          <Route path="/boxing" element={<BoxingProcess />} />
          <Route path="/master-boxing" element={<MasterBoxing />} />
          <Route path="/reports" element={<ReportsScreen />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
