import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "@components/layout/Sidebar";
import Dashboard from "@pages/Dashboard";
import LiveTracking from "@pages/LiveTracking";
import SignalAnalytics from "@pages/SignalAnalytics";
import Training from "@pages/Training";
import Calibration from "@pages/Calibration";
import Settings from "@pages/Settings";
import "./styles/globals.css";

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-slate-950">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/tracking" element={<LiveTracking />} />
            <Route path="/analytics" element={<SignalAnalytics />} />
            <Route path="/training" element={<Training />} />
            <Route path="/calibration" element={<Calibration />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
