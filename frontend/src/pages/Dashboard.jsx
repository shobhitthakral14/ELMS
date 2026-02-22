import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getMyLeaveBalances, getLeaveRequests, getPendingApprovals } from '../services/api/api'
import './Dashboard.css'

function Dashboard({ user }) {
  const [balances, setBalances] = useState([])
  const [requests, setRequests] = useState([])
  const [pendingApprovals, setPendingApprovals] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      const [balancesData, requestsData] = await Promise.all([
        getMyLeaveBalances(),
        getLeaveRequests(),
      ])

      setBalances(balancesData)
      setRequests(requestsData.slice(0, 5))

      if (user.role === 'manager' || user.role === 'hr_admin') {
        const approvalsData = await getPendingApprovals()
        setPendingApprovals(approvalsData)
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Welcome, {user.full_name}!</h2>
        <p className="role-badge">{user.role.replace('_', ' ').toUpperCase()}</p>
      </div>

      <div className="dashboard-grid">
        {/* Leave Balances */}
        <div className="card">
          <h3>Your Leave Balances</h3>
          {balances.length > 0 ? (
            <div className="balance-list">
              {balances.map((balance) => (
                <div key={balance.id} className="balance-item">
                  <div className="balance-name">{balance.leave_type_name}</div>
                  <div className="balance-stats">
                    <span className="stat">
                      <strong>{balance.available_days}</strong> Available
                    </span>
                    <span className="stat">
                      <strong>{balance.used_days}</strong> Used
                    </span>
                    <span className="stat">
                      <strong>{balance.pending_days}</strong> Pending
                    </span>
                  </div>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${(balance.used_days / balance.total_days) * 100}%`,
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No leave balances available</p>
          )}
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h3>Quick Actions</h3>
          <div className="action-buttons">
            <Link to="/leave-request" className="action-btn">
              <span className="icon">📝</span>
              <span>New Leave Request</span>
            </Link>
            <Link to="/leave-list" className="action-btn">
              <span className="icon">📋</span>
              <span>My Leave Requests</span>
            </Link>
            {(user.role === 'manager' || user.role === 'hr_admin') && (
              <Link to="/approvals" className="action-btn">
                <span className="icon">✅</span>
                <span>
                  Pending Approvals
                  {pendingApprovals.length > 0 && (
                    <span className="badge">{pendingApprovals.length}</span>
                  )}
                </span>
              </Link>
            )}
          </div>
        </div>

        {/* Recent Requests */}
        <div className="card full-width">
          <h3>Recent Leave Requests</h3>
          {requests.length > 0 ? (
            <div className="request-table">
              <table>
                <thead>
                  <tr>
                    <th>Leave Type</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Days</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {requests.map((request) => (
                    <tr key={request.id}>
                      <td>{request.leave_type_name}</td>
                      <td>{new Date(request.start_date).toLocaleDateString()}</td>
                      <td>{new Date(request.end_date).toLocaleDateString()}</td>
                      <td>{request.total_days}</td>
                      <td>
                        <span className={`status-badge status-${request.status}`}>
                          {request.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>No leave requests yet</p>
          )}
          <Link to="/leave-list" className="view-all">
            View All Requests →
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
