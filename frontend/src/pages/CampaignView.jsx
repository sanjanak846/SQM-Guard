import React, { useEffect, useState } from "react";
import { getCampaigns } from "../api/client";

export default function CampaignView() {
  const [campaigns, setCampaigns] = useState([]);

  useEffect(() => {
    getCampaigns()
      .then((res) => setCampaigns(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h2>Detected Multi-Stage Attack Campaigns</h2>
      {campaigns.length === 0 && <p>No campaigns detected yet.</p>}
      {campaigns.map((c, i) => (
        <div key={i} style={{ border: "1px solid #ccc", borderRadius: "8px", padding: "15px", marginBottom: "15px" }}>
          <h4>Campaign {i + 1}</h4>
          <p><strong>Linked Alert IDs:</strong> {c.alert_ids.join(", ")}</p>
          <p><strong>Attack Progression (MITRE ATT&CK tactics):</strong></p>
          <div style={{ display: "flex", gap: "8px" }}>
            {c.tactics.map((tactic, idx) => (
              <span key={idx} style={{ background: "#3498db", color: "white", padding: "4px 10px", borderRadius: "6px" }}>
                {tactic} {idx < c.tactics.length - 1 && "→"}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}