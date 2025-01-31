import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import LoginPage from './screen/LoginPage';
import AttendanceForm from './screen/AttendanceForm';
import Administrator from './screen/Administrator';
import Progress from './screen/Progress'; // Import NewEvent component
import SuccessPage from './screen/SuccessPage';

function App() {
  // Check for JWT token and login type in localStorage
  const jwtToken = localStorage.getItem('jwtToken');
  const loginType = localStorage.getItem('loginType');

  const isAuthenticated = !!jwtToken;

  return (
    <Router>
      <Routes>
        {/* Root route: Redirect based on authentication and login type */}
        <Route path="/" element={
          isAuthenticated 
            ? (loginType === 'google' ? <Navigate to="/attendance" replace /> : <Navigate to="/administrator" replace />)
            : <LoginPage />
        } />

        {/* Attendance route: Accessible only to Google login */}
        <Route path="/attendance" element={
          isAuthenticated && loginType === 'google' 
            ? <AttendanceForm /> 
            : <Navigate to={loginType === 'traditional' ? "/administrator" : "/"} replace />
        } />

        {/* Administrator route: Accessible only to traditional login */}
        <Route path="/administrator" element={
          isAuthenticated && loginType === 'traditional' 
            ? <Administrator /> 
            : <Navigate to="/" replace />
        } />

        {/* Progress page: Open without JWT authentication */}
        <Route path="/progress" element={<Progress />} />

        {/* Progress page: Open without JWT authentication */}
        <Route path="/success" element={<SuccessPage />} />

        {/* Catch-all route for unauthorized access - Redirect to root */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;