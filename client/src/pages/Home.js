import React, { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";

const Home = () => {
  /**
   * Home
   * - used as a hub for redirecting the user to a right page
   */
  const [redirect, setRedirect] = useState(null);

  // Check user from the session storage and redirect to a right page
  useEffect(() => {
    let _user = JSON.parse(sessionStorage.getItem("user_info"));

    if (_user) {
      if (_user.status === "teamlead") {
        setRedirect("/access-form");
      } else if (_user.status === "member") {
        setRedirect("/member-detail");
      } else {
        setRedirect("/interest-form");
      }

      // User logged in
    } else {
      setRedirect("/login");
    }
  }, []);

  if (redirect) {
    return <Navigate to={redirect} replace={true} />;
  }

  return (
    <>
      <h1>Home Page</h1>
    </>
  );
};

export default Home;
