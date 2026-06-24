import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Services from './pages/Services';
import Environments from './pages/Environments';
import Pipelines from './pages/Pipelines';
import Builds from './pages/Builds';
import Deployments from './pages/Deployments';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('token');
  if (!token) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/services" element={<ProtectedRoute><Services /></ProtectedRoute>} />
        <Route path="/environments" element={<ProtectedRoute><Environments /></ProtectedRoute>} />
        <Route path="/pipelines" element={<ProtectedRoute><Pipelines /></ProtectedRoute>} />
        <Route path="/builds" element={<ProtectedRoute><Builds /></ProtectedRoute>} />
        <Route path="/deployments" element={<ProtectedRoute><Deployments /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
