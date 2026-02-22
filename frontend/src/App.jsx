import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import LeaveRequest from './pages/LeaveRequest'
import LeaveList from './pages/LeaveList'
import Approvals from './pages/Approvals'
import { ROUTES } from './constants/routes'
import { STORAGE_KEYS } from './constants/api'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN)
    const userData = localStorage.getItem(STORAGE_KEYS.USER)
    if (token && userData) {
      setUser(JSON.parse(userData))
    }
    setLoading(false)
  }, [])

  const handleLogin = (userData) => {
    setUser(userData)
  }

  const handleLogout = () => {
    localStorage.removeItem(STORAGE_KEYS.TOKEN)
    localStorage.removeItem(STORAGE_KEYS.USER)
    setUser(null)
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <Router>
      <div className="app">
        {user && (
          <nav className="navbar">
            <div className="nav-content">
              <h1>HR Leave Management System</h1>
              <div className="nav-right">
                <span className="user-info">
                  {user.full_name} ({user.role.replace('_', ' ').toUpperCase()})
                </span>
                <button onClick={handleLogout} className="btn btn-secondary">
                  Logout
                </button>
              </div>
            </div>
          </nav>
        )}

        <Routes>
          <Route
            path={ROUTES.LOGIN}
            element={!user ? <Login onLogin={handleLogin} /> : <Navigate to={ROUTES.DASHBOARD} />}
          />
          <Route
            path={ROUTES.DASHBOARD}
            element={user ? <Dashboard user={user} /> : <Navigate to={ROUTES.LOGIN} />}
          />
          <Route
            path={ROUTES.LEAVE_REQUEST}
            element={user ? <LeaveRequest user={user} /> : <Navigate to={ROUTES.LOGIN} />}
          />
          <Route
            path={ROUTES.LEAVE_LIST}
            element={user ? <LeaveList user={user} /> : <Navigate to={ROUTES.LOGIN} />}
          />
          <Route
            path={ROUTES.APPROVALS}
            element={
              user && (user.role === 'manager' || user.role === 'hr_admin') ? (
                <Approvals user={user} />
              ) : (
                <Navigate to={ROUTES.DASHBOARD} />
              )
            }
          />
          <Route path={ROUTES.HOME} element={<Navigate to={user ? ROUTES.DASHBOARD : ROUTES.LOGIN} />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
