# Frontend - HR Leave Management System

React + Vite frontend for the employee leave management system.

## 📁 Project Structure

```
frontend/
├── public/                      # Static assets
├── src/
│   ├── pages/                   # Page components (routes)
│   │   ├── Login.jsx           # Login page
│   │   ├── Login.css           # Login styles
│   │   ├── Dashboard.jsx       # Main dashboard
│   │   ├── Dashboard.css       # Dashboard styles
│   │   ├── LeaveRequest.jsx    # Submit leave request
│   │   ├── LeaveRequest.css    # Leave request styles
│   │   ├── LeaveList.jsx       # View leave requests
│   │   ├── LeaveList.css       # Leave list styles
│   │   ├── Approvals.jsx       # Approve/reject requests
│   │   └── Approvals.css       # Approvals styles
│   │
│   ├── components/              # Reusable UI components
│   │   └── (original components, can be removed)
│   │
│   ├── services/                # API and business logic
│   │   └── api/
│   │       └── api.js          # API client and endpoints
│   │
│   ├── constants/               # Configuration constants
│   │   ├── api.js              # API endpoints and config
│   │   └── routes.js           # Route paths
│   │
│   ├── hooks/                   # Custom React hooks (future)
│   │
│   ├── App.jsx                  # Main app component
│   ├── App.css                  # Main app styles
│   ├── main.jsx                 # Application entry point
│   └── index.css                # Global styles
│
├── index.html                   # HTML template
├── package.json                 # Dependencies and scripts
├── vite.config.js              # Vite configuration
└── README.md                    # This file
```

## 🚀 Quick Start

### Install Dependencies
```bash
cd frontend
npm install
```

### Run Development Server
```bash
npm run dev
```

The app will start on http://localhost:3000

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## 📂 Folder Organization

### `/src/pages/`
**Purpose**: Main page components that correspond to routes

Each page is self-contained with:
- Component logic (`.jsx`)
- Component styles (`.css`)

**Current Pages**:
- `Login` - Authentication page
- `Dashboard` - Main overview
- `LeaveRequest` - Submit new request
- `LeaveList` - View all requests
- `Approvals` - Manager/HR approval queue

### `/src/services/`
**Purpose**: External service integrations

- `api/` - Backend API client
  - Axios configuration
  - API endpoint definitions
  - Request/response handling

### `/src/constants/`
**Purpose**: Application-wide constants

- `api.js` - API endpoints, base URL, storage keys
- `routes.js` - Route paths and access control

### `/src/hooks/`
**Purpose**: Custom React hooks (for future use)

Examples:
- `useAuth()` - Authentication state
- `useLeaveBalance()` - Fetch leave balances
- `useApi()` - Generic API hook

### `/src/components/`
**Purpose**: Reusable UI components (for future)

Examples:
- Button, Card, Modal
- LeaveCard, BalanceCard
- Navbar, Sidebar

## 🎨 Styling Approach

### Current: Component-Level CSS
Each page has its own CSS file for isolation.

### Global Styles
- `index.css` - Global resets, utilities, button styles
- `App.css` - App-level styles (navbar, layout)

### CSS Organization
```css
/* Component-specific (LeaveList.css) */
.leave-list-container { }
.request-card { }

/* Global utilities (index.css) */
.btn { }
.error-message { }
.status-badge { }
```

## 🔌 API Integration

### Configuration
Edit `src/constants/api.js`:
```javascript
export const API_BASE_URL = 'http://localhost:8001';
```

### Usage in Components
```javascript
import { getLeaveRequests, createLeaveRequest } from '../services/api/api';

// Fetch data
const requests = await getLeaveRequests();

// Submit data
const newRequest = await createLeaveRequest({
  leave_type_id: 1,
  start_date: '2024-01-01',
  end_date: '2024-01-05'
});
```

### Available API Functions
See `src/services/api/api.js` for all available functions:
- Authentication: `login()`, `getCurrentUser()`
- Leave Types: `getLeaveTypes()`
- Balances: `getMyLeaveBalances()`
- Requests: `createLeaveRequest()`, `getLeaveRequests()`
- Approvals: `approveLeaveRequest()`, `rejectLeaveRequest()`

## 🛣️ Routing

### Route Definition
Routes are defined in `App.jsx` using React Router:

```javascript
<Route path="/dashboard" element={<Dashboard />} />
```

### Route Constants
Use constants from `src/constants/routes.js`:

```javascript
import { ROUTES } from './constants/routes';

navigate(ROUTES.DASHBOARD);
```

### Protected Routes
Routes automatically redirect to login if not authenticated.

## 🔐 Authentication

### Storage
- **Token**: `localStorage.getItem('token')`
- **User**: `localStorage.getItem('user')`

### Login Flow
1. User submits credentials
2. Backend returns JWT token
3. Token stored in localStorage
4. User info fetched and stored
5. App re-renders with user context

### Logout Flow
1. Clear localStorage
2. Reset user state
3. Redirect to login

## 🎯 Key Features by Page

### Dashboard
- Leave balance overview
- Quick action buttons
- Recent requests summary
- Pending approvals count (managers)

### Leave Request
- Leave type selection
- Date picker (start/end)
- Automatic working day calculation
- Balance availability check
- Form validation

### Leave List
- All user's requests
- Filter by status (All/Pending/Approved/Rejected)
- Cancel pending requests
- Status badges

### Approvals (Manager/HR Only)
- Pending approval queue
- Request details view
- Approve/reject actions
- Comment field (required for rejection)

## 🎨 UI Components

### Buttons
```javascript
<button className="btn btn-primary">Submit</button>
<button className="btn btn-secondary">Cancel</button>
<button className="btn btn-success">Approve</button>
<button className="btn btn-danger">Reject</button>
```

### Status Badges
```javascript
<span className="status-badge status-pending">Pending</span>
<span className="status-badge status-approved">Approved</span>
<span className="status-badge status-rejected">Rejected</span>
```

### Form Elements
```javascript
<div className="form-group">
  <label>Field Label</label>
  <input type="text" />
</div>
```

## 📱 Responsive Design

All pages are mobile-responsive with breakpoints:
- Desktop: > 768px
- Mobile: < 768px

## 🔧 Development Tips

### Hot Reload
Changes to `.jsx` and `.css` files trigger automatic reload.

### Debugging
- React DevTools: Inspect component tree
- Network tab: Monitor API calls
- Console: View API responses

### Adding a New Page

1. **Create page component**:
```javascript
// src/pages/NewPage.jsx
import './NewPage.css';

function NewPage() {
  return <div>New Page</div>;
}

export default NewPage;
```

2. **Add route**:
```javascript
// src/App.jsx
import NewPage from './pages/NewPage';

<Route path="/new-page" element={<NewPage />} />
```

3. **Add route constant**:
```javascript
// src/constants/routes.js
export const ROUTES = {
  NEW_PAGE: '/new-page',
  // ...
};
```

## 🐛 Common Issues

### API Connection Failed
- Check backend is running on port 8001
- Verify `API_BASE_URL` in `src/constants/api.js`
- Check CORS configuration in backend

### Token Expired
- Tokens expire after 24 hours
- User will be redirected to login automatically

### Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📦 Dependencies

### Core
- `react` - UI framework
- `react-dom` - DOM rendering
- `react-router-dom` - Routing

### HTTP Client
- `axios` - API requests

### Dev Tools
- `vite` - Build tool
- `@vitejs/plugin-react` - React support

## 🚀 Deployment

### Build
```bash
npm run build
```

Output: `dist/` folder

### Deploy to Static Hosting
- Netlify
- Vercel
- AWS S3 + CloudFront
- GitHub Pages

### Environment Variables
Create `.env` file:
```
VITE_API_URL=https://api.yourdomain.com
```

Access in code:
```javascript
const API_URL = import.meta.env.VITE_API_URL;
```

---

**Backend Integration**: This frontend connects to the FastAPI backend at http://localhost:8001
