import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import AlertQueue from "./pages/AlertQueue";
import AlertDetail from "./pages/AlertDetail";
import CampaignView from "./pages/CampaignView";

function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: "15px", background: "#2c3e50" }}>
        <Link to="/" style={{ color: "white", marginRight: "20px" }}>Alert Queue</Link>
        <Link to="/campaigns" style={{ color: "white" }}>Campaigns</Link>
      </nav>
      <Routes>
        <Route path="/" element={<AlertQueue />} />
        <Route path="/alerts/:id" element={<AlertDetail />} />
        <Route path="/campaigns" element={<CampaignView />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;