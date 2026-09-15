import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getAlerts } from "../api/client";

function riskColor(score) {
  if (score >= 70) return "#e74c3c";
  if (score >= 45) return "#f39c12";
  return "#2ecc71";
}

export default function AlertQueue() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAlerts()
      .then((res) => {
        const sorted = res.data.sort((a, b) => (b.risk_score || 0) - (a.risk_score || 0));
        setAlerts(sorted);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading alerts...</p>;

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h2>SQM-Guard — Alert Queue</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ borderBottom: "2px solid #333" }}>
            <th>ID</th>
            <th>Timestamp</th>
            <th>Status</th>
            <th>Risk Score</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((alert) => (
            <tr key={alert.id} style={{ borderBottom: "1px solid #ddd" }}>
              <td>{alert.id}</td>
              <td>{new Date(alert.timestamp).toLocaleString()}</td>
              <td>{alert.status}</td>
              <td>
                <span
                  style={{
                    padding: "4px 10px",
                    borderRadius: "6px",
                    color: "white",
                    background: riskColor(alert.risk_score || 0),
                  }}
                >
                  {alert.risk_score ?? "N/A"}
                </span>
              </td>
              <td>
                <Link to={`/alerts/${alert.id}`}>View Details</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}