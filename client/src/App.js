import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./style.css";

import Home from "./pages/Home";
import Login from "./pages/Login";
import InterestForm from "./pages/interestForm";
import AccessForm from "./pages/accessForm";
import MemberDetailForm from "./pages/memberDetailForm";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />

        <Route
          path="/interest-form"
          element={
            <ProtectedRoute statusType={"new"}>
              <InterestForm />
            </ProtectedRoute>
          }
        />

        <Route
          path="/access-form"
          element={
            <ProtectedRoute statusType={"teamlead"}>
              <AccessForm />
            </ProtectedRoute>
          }
        />

        <Route
          path="/member-detail"
          element={
            <ProtectedRoute statusType={"member"}>
              <MemberDetailForm />
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<p>There's nothing here: 404!</p>} />
      </Routes>
    </Router>
  );
};

export default App;
