/**
 * Application Route Constants
 */

export const ROUTES = {
  // Public routes
  LOGIN: '/login',

  // Private routes
  DASHBOARD: '/dashboard',
  LEAVE_REQUEST: '/leave-request',
  LEAVE_LIST: '/leave-list',
  APPROVALS: '/approvals',

  // Default
  HOME: '/',
};

export const PUBLIC_ROUTES = [ROUTES.LOGIN];

export const PRIVATE_ROUTES = [
  ROUTES.DASHBOARD,
  ROUTES.LEAVE_REQUEST,
  ROUTES.LEAVE_LIST,
  ROUTES.APPROVALS,
];

export const MANAGER_ONLY_ROUTES = [ROUTES.APPROVALS];
