import React, { useState } from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children, statusType }) => {
  /*
  Protected Route
  - used to check if the user type is matching with the current route that user is trying to visit
  - redirect to login or error page if user type is not matching with the current route
  - redirect to login when not logged in (user does not exist in session storage)
  - redirect to error when user type does not match with the current route

  User Types
  - teamlead
  - new (new student)
  - member (a student who already submitted interest form)
  */



  // Get User Info from the session storage
  const [user, setUser] = useState(
    JSON.parse(sessionStorage.getItem("user_info"))
  );

  // Check User
  // If no user in session storage redirect to Home "/"
  if (!user) {
    return <Navigate to="/" replace={true} />;
    // If user type matches with the current route, render the current route
  } else if (user.status === statusType) {
    return children;
    // If user type does not match with the current route, send to error page
  } else {
    return <Navigate to="/error" replace={true} />;
  }
};

export default ProtectedRoute;
