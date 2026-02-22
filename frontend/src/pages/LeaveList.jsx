import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getLeaveRequests, cancelLeaveRequest } from '../services/api/api'
import './LeaveList.css'

function LeaveList() {
  const navigate = useNavigate()
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    loadRequests()
  }, [])

  const loadRequests = async () => {
    setLoading(true)
    try {
      const data = await getLeaveRequests()
      setRequests(data)
    } catch (err) {
      setError('Failed to load leave requests')
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (id) => {
    if (!window.confirm('Are you sure you want to cancel this leave request?')) {
      return
    }

    try {
      await cancelLeaveRequest(id)
      await loadRequests()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to cancel request')
    }
  }

  const filteredRequests = requests.filter((req) => {
    if (filter === 'all') return true
    return req.status === filter
  })

  if (loading) {
    return <div className="loading">Loading requests...</div>
  }

  return (
    <div className="leave-list-container">
      <div className="page-header">
        <div>
          <h2>My Leave Requests</h2>
          <p>View and manage your leave requests</p>
        </div>
        <div className="header-actions">
          <button onClick={() => navigate('/leave-request')} className="btn btn-primary">
            + New Request
          </button>
          <button onClick={() => navigate('/dashboard')} className="btn btn-secondary">
            ← Dashboard
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="filter-bar">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All ({requests.length})
        </button>
        <button
          className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
          onClick={() => setFilter('pending')}
        >
          Pending ({requests.filter((r) => r.status === 'pending').length})
        </button>
        <button
          className={`filter-btn ${filter === 'approved' ? 'active' : ''}`}
          onClick={() => setFilter('approved')}
        >
          Approved ({requests.filter((r) => r.status === 'approved').length})
        </button>
        <button
          className={`filter-btn ${filter === 'rejected' ? 'active' : ''}`}
          onClick={() => setFilter('rejected')}
        >
          Rejected ({requests.filter((r) => r.status === 'rejected').length})
        </button>
      </div>

      {filteredRequests.length > 0 ? (
        <div className="requests-grid">
          {filteredRequests.map((request) => (
            <div key={request.id} className="request-card">
              <div className="request-header">
                <span className={`status-badge status-${request.status}`}>{request.status}</span>
                <span className="request-id">#{request.id}</span>
              </div>

              <div className="request-body">
                <div className="request-info">
                  <div className="info-item">
                    <span className="info-label">Leave Type:</span>
                    <span className="info-value">{request.leave_type_name}</span>
                  </div>

                  <div className="info-item">
                    <span className="info-label">Duration:</span>
                    <span className="info-value">
                      {new Date(request.start_date).toLocaleDateString()} to{' '}
                      {new Date(request.end_date).toLocaleDateString()}
                    </span>
                  </div>

                  <div className="info-item">
                    <span className="info-label">Total Days:</span>
                    <span className="info-value">{request.total_days} days</span>
                  </div>

                  {request.reason && (
                    <div className="info-item">
                      <span className="info-label">Reason:</span>
                      <span className="info-value">{request.reason}</span>
                    </div>
                  )}

                  <div className="info-item">
                    <span className="info-label">Submitted:</span>
                    <span className="info-value">
                      {new Date(request.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>

              {request.status === 'pending' && (
                <div className="request-actions">
                  <button
                    onClick={() => handleCancel(request.id)}
                    className="btn btn-danger btn-sm"
                  >
                    Cancel Request
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <p>No leave requests found</p>
          <button onClick={() => navigate('/leave-request')} className="btn btn-primary">
            Submit Your First Request
          </button>
        </div>
      )}
    </div>
  )
}

export default LeaveList
