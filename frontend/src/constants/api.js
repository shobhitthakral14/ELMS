/**
 * API Configuration Constants
 */

// Base URL for the backend API
export const API_BASE_URL = 'http://localhost:8001';

// API Endpoints
export const API_ENDPOINTS = {
  // Authentication
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  ME: '/auth/me',

  // Users
  USERS: '/users',
  USER_TEAM: (id) => `/users/${id}/team`,

  // Leave Types
  LEAVE_TYPES: '/leave-types',

  // Leave Balances
  MY_BALANCES: '/leave-balances/me',
  USER_BALANCES: (userId) => `/leave-balances/${userId}`,
  INITIALIZE_BALANCES: (year) => `/leave-balances/initialize/${year}`,

  // Leave Requests
  LEAVE_REQUESTS: '/leave-requests',
  LEAVE_REQUEST: (id) => `/leave-requests/${id}`,
  PENDING_APPROVALS: '/leave-requests/pending-approvals',

  // Approvals
  APPROVE: (id) => `/approvals/${id}/approve`,
  REJECT: (id) => `/approvals/${id}/reject`,
  MY_PENDING: '/approvals/my-pending',

  // Holidays
  HOLIDAYS: '/holidays',
  HOLIDAY: (id) => `/holidays/${id}`,
  HOLIDAYS_BY_YEAR: (year) => `/holidays/${year}`,

  // Delegations
  DELEGATIONS: '/delegations',
  ACTIVE_DELEGATIONS: '/delegations/active',
  DELEGATION: (id) => `/delegations/${id}`,

  // Reports
  TEAM_CALENDAR: '/reports/team-calendar',
  LEAVE_SUMMARY: '/reports/leave-summary',
  PENDING_REQUESTS: '/reports/pending-requests',
  USER_HISTORY: (userId) => `/reports/user-leave-history/${userId}`,
};

// Storage Keys
export const STORAGE_KEYS = {
  TOKEN: 'token',
  USER: 'user',
};
