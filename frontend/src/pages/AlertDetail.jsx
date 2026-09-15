import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getAlert, resolveAlert, approveAlert, rejectAlert, getHistory } from "../api/client";

export default function AlertDetail() {
  const { id } = useParams();
  const [alert, setAlert] = useState(null);
  const [resolution, setResolution] = useState(null);
  const [history, setHistory] = useState([]);
  const [comment, setComment] = useState("");

  const loadAlert = () => {
    getAlert(id).then((res) => setAlert(res.data));
    getHistory(id).then((res) => setHistory(res.data));
  };

  useEffect(() => {
    loadAlert();
  }, [id]);

  const handleAnalyze = () => {
    resolveAlert(id).then((res) => setResolution(res.data));
  };

  const handleApprove = () => {
    approveAlert(id, comment).then(() => loadAlert());
  };

  const handleReject = () => {
    rejectAlert(id, comment).then(() => loadAlert());
  };

  if (!alert) return <p>Loading...</p>;

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif", maxWidth: "800px" }}>
      <h2>Alert #{alert.id}</h2>
      <p><strong>Status:</strong> {alert.status}</p>
      <p><strong>Timestamp:</strong> {new Date(alert.timestamp).toLocaleString()}</p>

      <h3>Raw Log Data</h3>
      <pre style={{ background: "#f4f4f4", padding: "10px", borderRadius: "6px" }}>
        {JSON.stringify(alert.raw_fields, null, 2)}
      </pre>

      <button onClick={handleAnalyze} style={{ padding: "8px 16px", marginBottom: "15px" }}>
        Run Full Analysis
      </button>

      {resolution && (
        <div style={{ background: "#eef6ff", padding: "15px", borderRadius: "8px" }}>
          <h3>Risk Assessment</h3>
          <p><strong>Risk Score:</strong> {resolution.risk_score}</p>
          <p><strong>Contributing Factors:</strong></p>
          <ul>
            <li>Anomaly Score: {resolution.contributing_factors?.anomaly_score}</li>
            <li>Injection Detected: {String(resolution.contributing_factors?.injection_detected)}</li>
            <li>Query Repair Attempts: {resolution.contributing_factors?.query_repair_attempts}</li>
          </ul>
          <h3>Resolution Recommendation</h3>
          <p><strong>Category:</strong> {resolution.resolution?.category}</p>
          <p><strong>Justification:</strong> {resolution.resolution?.justification}</p>
        </div>
      )}

      <h3 style={{ marginTop: "20px" }}>Analyst Decision</h3>
      <input
        type="text"
        placeholder="Optional comment"
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
      />
      <button onClick={handleApprove} style={{ marginRight: "10px", padding: "8px 16px", background: "#2ecc71", color: "white" }}>
        Approve
      </button>
      <button onClick={handleReject} style={{ padding: "8px 16px", background: "#e74c3c", color: "white" }}>
        Reject
      </button>

      <h3 style={{ marginTop: "20px" }}>Audit Trail</h3>
      <ul>
        {history.map((h, i) => (
          <li key={i}>
            {new Date(h.timestamp).toLocaleString()} — {h.from_status} → {h.to_status}
            {h.comment && ` ("${h.comment}")`}
          </li>
        ))}
      </ul>
    </div>
  );
}