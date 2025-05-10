import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import { useEffect } from "react";

import HelloPage from "./HelloPage.jsx";
import HomePage from "./HomePage.jsx";
import CalibratePage from "./CalibratePage.jsx";
import LivestreamPage from "./LivestreamPage.jsx";
import PreviousDeterrentsPage from "./PreviousDeterrentsPage.jsx";
import WarningPage from "./WarningPage.jsx";

// Wrapper to handle auto-redirect on alert
function AppWrapper() {
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch("http://raspberrypi.local:5000/alert"); // Replace with real endpoint
        const data = await res.json();
        if (data.alert === true) {
          navigate("/warning");
        }
      } catch (err) {
        console.error("Error checking for alerts:", err);
      }
    }, 3000); // Check every 3 seconds

    return () => clearInterval(interval);
  }, [navigate]);

  return (
    <Routes>
      <Route path="/" element={<HelloPage />} />
      <Route path="/home" element={<HomePage />} />
      <Route path="/calibrate" element={<CalibratePage />} />
      <Route path="/livestream" element={<LivestreamPage />} />
      <Route path="/deterrents" element={<PreviousDeterrentsPage />} />
      <Route path="/warning" element={<WarningPage />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppWrapper />
    </BrowserRouter>
  );
}