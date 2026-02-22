import { useState } from 'react'
import { login, getCurrentUser } from '../services/api/api'
import { STORAGE_KEYS } from '../constants/api'
import './Login.css'

function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const { access_token } = await login(email, password)
      localStorage.setItem(STORAGE_KEYS.TOKEN, access_token)

      const user = await getCurrentUser()
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user))

      onLogin(user)
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const quickLogin = async (testEmail, testPassword) => {
    setEmail(testEmail)
    setPassword(testPassword)
    setError('')
    setLoading(true)

    try {
      const { access_token } = await login(testEmail, testPassword)
      localStorage.setItem(STORAGE_KEYS.TOKEN, access_token)

      const user = await getCurrentUser()
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user))

      onLogin(user)
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>HR Leave Management System</h1>
        <h2>Login</h2>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="quick-login">
          <p>Quick Login (Demo):</p>
          <div className="quick-login-buttons">
            <button
              onClick={() => quickLogin('employee@company.com', 'employee123')}
              className="btn btn-secondary"
              disabled={loading}
            >
              Employee
            </button>
            <button
              onClick={() => quickLogin('manager@company.com', 'manager123')}
              className="btn btn-secondary"
              disabled={loading}
            >
              Manager
            </button>
            <button
              onClick={() => quickLogin('admin@company.com', 'admin123')}
              className="btn btn-secondary"
              disabled={loading}
            >
              HR Admin
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
