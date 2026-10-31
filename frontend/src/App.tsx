import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/Navbar/Navbar';
import { BottomNav } from './components/BottomNav/BottomNav';
import { Footer } from './components/Footer/Footer';
import { ScanPage } from './pages/ScanPage/ScanPage';
import { SignsPage } from './pages/SignsPage/SignsPage';
import { SignDetailPage } from './pages/SignDetailPage/SignDetailPage';
import { HistoryPage } from './pages/HistoryPage/HistoryPage';
import { EvaluationPage } from './pages/EvaluationPage/EvaluationPage';
import { AboutPage } from './pages/AboutPage/AboutPage';
import { api } from './api/client';
import type { HealthResponse } from './api/types';

export const App: React.FC = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState<boolean>(true);
  const [healthError, setHealthError] = useState<boolean>(false);

  useEffect(() => {
    let isMounted = true;
    setHealthLoading(true);

    api
      .getHealth()
      .then((data) => {
        if (isMounted) {
          setHealth(data);
          setHealthError(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          console.warn('Backend health check error:', err);
          setHealthError(true);
        }
      })
      .finally(() => {
        if (isMounted) {
          setHealthLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <>
      <Navbar
        health={health}
        healthLoading={healthLoading}
        healthError={healthError}
      />

      <main style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Routes>
          <Route path="/" element={<ScanPage health={health} />} />
          <Route path="/signs" element={<SignsPage />} />
          <Route path="/signs/:id" element={<SignDetailPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/evaluation" element={<EvaluationPage />} />
          <Route path="/about" element={<AboutPage health={health} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      <Footer />
      <BottomNav />
    </>
  );
};

export default App;
