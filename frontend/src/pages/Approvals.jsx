import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getPendingApprovals, approveLeaveRequest, rejectLeaveRequest } from '../services/api/api'
import './Approvals.css'

function Approvals() {
  const navigate = useNavigate()
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [actionLoading, setActionLoading] = useState(null)
  const [comments, setComments] = useState({})

  useEffect(() => {
    loadRequests()
  }, [])

  const loadRequests = async () => {
    setLoading(true)
    try {
      const data = await getPendingApprovals()
      setRequests(data)
    } catch (err) {
      setError('Failed to load pending approvals')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (id) => {
    if (!window.confirm('Are you sure you want to approve this leave request?')) {
      return
    }

    setActionLoading(id)
    try {
      await approveLeaveRequest(id, comments[id] || '')
      await loadRequests()
      setComments({ ...comments, [id]: '' })
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to approve request')
    } finally {
      setActionLoading(null)
    }
  }

  const handleReject = async (id) => {
    if (!window.confirm('Are you sure you want to reject this leave request?')) {
      return
    }

    if (!comments[id]) {
      setError('Please provide comments for rejection')
      return
    }

    setActionLoading(id)
    try {
      await rejectLeaveRequest(id, comments[id])
      await loadRequests()
      setComments({ ...comments, [id]: '' })
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reject request')
    } finally {
      setActionLoading(null)
    }
  }

  const handleCommentChange = (id, value) => {
    setComments({
      ...comments,
      [id]: value,
    })
  }

  if (loading) {
    return <div className="loading">Loading pending approvals...</div>
  }

  return (
    <div className="approvals-container">
      <div className="page-header">
        <div>
          <h2>Pending Approvals</h2>
          <p>Review and approve leave requests</p>
        </div>
        <button onClick={() => navigate('/dashboard')} className="btn btn-secondary">
          ← Dashboard
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {requests.length > 0 ? (
        <div className="approvals-list">
          {requests.map((request) => (
            <div key={request.id} className="approval-card">
              <div className="approval-header">
                <div>
                  <h3>{request.user_name}</h3>
                  <span className="request-id">Request #{request.id}</span>
                </div>
                <span className={`status-badge status-${request.status}`}>{request.status}</span>
              </div>

              <div className="approval-body">
                <div className="approval-details">
                  <div className="detail-row">
                    <div className="detail-item">
                      <span className="detail-label">Leave Type</span>
                      <span className="detail-value">{request.leave_type_name}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Duration</span>
                      <span className="detail-value">{request.total_days} days</span>
                    </div>
                  </div>

                  <div className="detail-row">
                    <div className="detail-item">
                      <span className="detail-label">Start Date</span>
                      <span className="detail-value">
                        {new Date(request.start_date).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">End Date</span>
                      <span className="detail-value">
                        {new Date(request.end_date).toLocaleDateString()}
                      </span>
                    </div>
                  </div>

                  {request.reason && (
                    <div className="detail-row full-width">
                      <div className="detail-item">
                        <span className="detail-label">Reason</span>
                        <span className="detail-value">{request.reason}</span>
                      </div>
                    </div>
                  )}

                  <div className="detail-row full-width">
                    <div className="detail-item">
                      <span className="detail-label">Submitted On</span>
                      <span className="detail-value">
                        {new Date(request.created_at).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="approval-actions">
                  <div className="comments-section">
                    <label>Comments (Required for rejection):</label>
                    <textarea
                      value={comments[request.id] || ''}
                      onChange={(e) => handleCommentChange(request.id, e.target.value)}
                      placeholder="Add your comments here..."
                      rows="3"
                    />
                  </div>

                  <div className="action-buttons">
                    <button
                      onClick={() => handleReject(request.id)}
                      className="btn btn-danger"
                      disabled={actionLoading === request.id}
                    >
                      {actionLoading === request.id ? 'Processing...' : 'Reject'}
                    </button>
                    <button
                      onClick={() => handleApprove(request.id)}
                      className="btn btn-success"
                      disabled={actionLoading === request.id}
                    >
                      {actionLoading === request.id ? 'Processing...' : 'Approve'}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <p>No pending approvals at the moment</p>
          <button onClick={() => navigate('/dashboard')} className="btn btn-primary">
            Back to Dashboard
          </button>
        </div>
      )}
    </div>
  )
}

export default Approvals
