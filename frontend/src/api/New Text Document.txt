import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const getAlerts = () => axios.get(`${API_BASE}/alerts`);
export const getAlert = (id) => axios.get(`${API_BASE}/alerts/${id}`);
export const resolveAlert = (id) => axios.post(`${API_BASE}/alerts/${id}/resolve`);
export const approveAlert = (id, comment) => axios.post(`${API_BASE}/alerts/${id}/approve`, null, { params: { comment } });
export const rejectAlert = (id, comment) => axios.post(`${API_BASE}/alerts/${id}/reject`, null, { params: { comment } });
export const getHistory = (id) => axios.get(`${API_BASE}/alerts/${id}/history`);
export const getCampaigns = () => axios.get(`${API_BASE}/campaigns`);