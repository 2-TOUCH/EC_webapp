import React, { useState, useEffect } from "react";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import jwt_decode from "jwt-decode";
import { Navigate } from "react-router-dom";

const Login = () => {
  const [redirect, setRedirect] = useState(null);

  // Check Session Storage to see if user already logged in
  // Redirect to right page when already logged in
  useEffect(() => {
    let userInfo = JSON.parse(sessionStorage.getItem("user_info"));

    if (typeof userInfo === "object" && userInfo !== null) {
      // Redirect to right page
      if (userInfo.status === "teamlead") {
        setRedirect("/access-form");
      } else if (userInfo.status === "member") {
        setRedirect("/member-detail");
      } else if (userInfo.status === "new") {
        setRedirect("/interest-form");
      }
    }
  }, []);

  // Redirect User if logged in
  if (redirect) {
    return <Navigate to={redirect} replace={true} />;
  }

  async function setUserInfo(credentialResponse) {
    const { email, family_name, given_name } = jwt_decode(
      credentialResponse.credential
    );
    const checkDavis = /@ucdavis\.edu$/;

    // User Not in UCDAVIS Email Address
    if (!checkDavis.test(email)) {
      alert(
        "Email does not belong to ucdavis.edu. Please Log in with UC DAVIS account"
      );
    }
    // Save User Status
    else {
      const leaderShipRoles = {
        DEIM: "DEI",
        PM: "PM",
        "SDI Subteam Leader": "SDI",
        "CAVs Subteam Leader": "CAV",
        "PCM Subteam Leader": "PCM",
        "HMI Subteam Leader": "HMI/UX",
        CM: "Communications",
      };

      try {
        // Try finding user in DB
        const url = `http://localhost:5000/member-detail/login?lastName=${family_name}&firstName=${given_name}`;
        let res = await fetch(url);
        let checkUser = await res.json();

        // User exists, set login status
        if (checkUser.success) {
          // Check if the user is a leader
          if (checkUser.data.leaderShipRole in leaderShipRoles) {
            sessionStorage.setItem(
              "user_info",
              JSON.stringify({ ...checkUser.data, status: "teamlead" }) // --> access-form
            );
          } else {
            sessionStorage.setItem(
              "user_info",
              JSON.stringify({ ...checkUser.data, status: "member" }) // --> member-detail
            );
          }
          setRedirect("/");
        }

        // User Does not Exist
        else if (res.status === 404) {
          console.log(given_name + " " + family_name);
          let user = {
            emailaddress: email,
            firstname: given_name,
            lastname: family_name,
          };
          sessionStorage.setItem(
            "user_info",
            JSON.stringify({ ...user, status: "new" }) // --> interest-form
          );
          // Resource not found
          setRedirect("/");
        }

        // Some weird Error
        else {
          // Other error status codes
          console.log(`Request failed with status code: ${res.status}`);
          setRedirect("/error");
        }
      } catch (e) {
        console.log(`Error with fetching user data: ${e.message}`);
        setRedirect("/error");
      }
    }
  }

  return (
    <div className="content">
      <div className="login">
        <h1>Welcome to ECOCAR UC DAVIS</h1>
        <p>Please Login with UC DAVIS account ^^</p>
        <GoogleOAuthProvider clientId="203619968227-oqi2isukcbmdc3dpuqvbhk0i6lponb2n.apps.googleusercontent.com">
          <GoogleLogin
            onSuccess={async (credentialResponse) => {
              await setUserInfo(credentialResponse);
            }}
            onError={() => {
              console.log("Login Failed");
            }}
          />
        </GoogleOAuthProvider>
      </div>
    </div>
  );
};

export default Login;
