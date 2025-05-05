import { BrowserRouter, Routes, Route } from "react-router-dom";
import HelloPage from "./HelloPage.jsx";
import HomePage from "./HomePage.jsx";
import CalibratePage from "./CalibratePage.jsx";
import LivestreamPage from "./LivestreamPage.jsx";
import PreviousDeterrentsPage from "./PreviousDeterrentsPage.jsx";
import WarningPage from "./WarningPage.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HelloPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/calibrate" element={<CalibratePage />} />
        <Route path="/livestream" element={<LivestreamPage />} />
        <Route path="/deterrents" element={<PreviousDeterrentsPage />} />
        <Route path="/warning" element={<WarningPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
