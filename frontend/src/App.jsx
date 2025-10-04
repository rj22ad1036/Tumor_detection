import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./pages/Auth/Login";
import PrivateRoute from "./Components/PrivateRoute";
import SuperadminHospitalPage from "./pages/hospital/dashboard";
import DoctorsListPage from "./pages/doctors/[id]/page";

// Placeholder dashboards
const HospitalDashboard = () => (
  <h1 className="text-center mt-10 text-2xl">Hospital Dashboard</h1>
);
const DoctorDashboard = () => (
  <h1 className="text-center mt-10 text-2xl">Doctor Dashboard</h1>
);
const PatientDashboard = () => (
  <h1 className="text-center mt-10 text-2xl">Patient Dashboard</h1>
);

function App() {
  return (
    <Router>
      <Routes>
        {/* Auth */}
        <Route path="/login" element={<Login />} />

        {/* Dashboards */}
        <Route
          path="/dashboard/superadmin"
          element={
            <PrivateRoute role="superadmin">
              <SuperadminHospitalPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/doctors/:id"
          element={
            <PrivateRoute role="superadmin">
              <DoctorsListPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/dashboard/hospital"
          element={
            <PrivateRoute role="hospital">
              <HospitalDashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/dashboard/doctor"
          element={
            <PrivateRoute role="doctor">
              <DoctorDashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/dashboard/patient"
          element={
            <PrivateRoute role="patient">
              <PatientDashboard />
            </PrivateRoute>
          }
        />

        {/* Default route */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
