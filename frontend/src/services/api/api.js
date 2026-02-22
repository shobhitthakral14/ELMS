import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const login = async (email, password) => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);

  const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

// Leave Types API
export const getLeaveTypes = async () => {
  const response = await api.get('/leave-types');
  return response.data;
};

// Leave Balances API
export const getMyLeaveBalances = async () => {
  const response = await api.get('/leave-balances/me');
  return response.data;
};

// Leave Requests API
export const createLeaveRequest = async (data) => {
  const response = await api.post('/leave-requests', data);
  return response.data;
};

export const getLeaveRequests = async () => {
  const response = await api.get('/leave-requests');
  return response.data;
};

export const cancelLeaveRequest = async (id) => {
  const response = await api.delete(`/leave-requests/${id}`);
  return response.data;
};

export const getPendingApprovals = async () => {
  const response = await api.get('/leave-requests/pending-approvals');
  return response.data;
};

// Approvals API
export const approveLeaveRequest = async (id, comments = '') => {
  const response = await api.post(`/approvals/${id}/approve`, { comments });
  return response.data;
};

export const rejectLeaveRequest = async (id, comments = '') => {
  const response = await api.post(`/approvals/${id}/reject`, { comments });
  return response.data;
};

// Holidays API
export const getHolidays = async () => {
  const response = await api.get('/holidays');
  return response.data;
};

export default api;
