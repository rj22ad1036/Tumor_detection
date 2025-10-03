import React from "react";
import { Navigate } from "react-router-dom";

interface PrivateRouteProps {
  role: string;
  children: React.ReactNode;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ role, children }) => {
  const token = localStorage.getItem("token");
  const userRole = localStorage.getItem("role");

  if (!token) return <Navigate to="/login" replace />;
  if (role && userRole?.toLowerCase() !== role.toLowerCase()) return <Navigate to="/login" replace />;

  return <>{children}</>;
};

export default PrivateRoute;
