import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getLeaveTypes, getMyLeaveBalances, createLeaveRequest } from '../services/api/api'
import './LeaveRequest.css'

function LeaveRequest() {
  const navigate = useNavigate()
  const [leaveTypes, setLeaveTypes] = useState([])
  const [balances, setBalances] = useState([])
  const [formData, setFormData] = useState({
    leave_type_id: '',
    start_date: '',
    end_date: '',
    reason: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [typesData, balancesData] = await Promise.all([
        getLeaveTypes(),
        getMyLeaveBalances(),
      ])
      setLeaveTypes(typesData)
      setBalances(balancesData)
    } catch (err) {
      setError('Failed to load leave types')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await createLeaveRequest({
        ...formData,
        leave_type_id: parseInt(formData.leave_type_id),
      })
      navigate('/leave-list')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit leave request')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const getAvailableBalance = () => {
    if (!formData.leave_type_id) return null
    const balance = balances.find((b) => b.leave_type_id === parseInt(formData.leave_type_id))
    return balance ? balance.available_days : 0
  }

  const availableBalance = getAvailableBalance()

  return (
    <div className="leave-request-container">
      <div className="page-header">
        <h2>Submit Leave Request</h2>
        <button onClick={() => navigate('/dashboard')} className="btn btn-secondary">
          ← Back to Dashboard
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="form-card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="leave_type_id">Leave Type *</label>
            <select
              id="leave_type_id"
              name="leave_type_id"
              value={formData.leave_type_id}
              onChange={handleChange}
              required
            >
              <option value="">Select leave type</option>
              {leaveTypes.map((type) => (
                <option key={type.id} value={type.id}>
                  {type.name}
                </option>
              ))}
            </select>
            {availableBalance !== null && (
              <small className="form-help">Available balance: {availableBalance} days</small>
            )}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="start_date">Start Date *</label>
              <input
                type="date"
                id="start_date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                min={new Date().toISOString().split('T')[0]}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="end_date">End Date *</label>
              <input
                type="date"
                id="end_date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                min={formData.start_date || new Date().toISOString().split('T')[0]}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="reason">Reason</label>
            <textarea
              id="reason"
              name="reason"
              value={formData.reason}
              onChange={handleChange}
              rows="4"
              placeholder="Enter the reason for your leave (optional)"
            />
          </div>

          <div className="form-actions">
            <button type="button" onClick={() => navigate('/dashboard')} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Submitting...' : 'Submit Request'}
            </button>
          </div>
        </form>
      </div>

      {balances.length > 0 && (
        <div className="balance-summary">
          <h3>Your Leave Balances</h3>
          <div className="balance-grid">
            {balances.map((balance) => (
              <div key={balance.id} className="balance-card">
                <div className="balance-card-header">{balance.leave_type_name}</div>
                <div className="balance-card-body">
                  <div className="balance-stat">
                    <span className="stat-value">{balance.available_days}</span>
                    <span className="stat-label">Available</span>
                  </div>
                  <div className="balance-stat">
                    <span className="stat-value">{balance.used_days}</span>
                    <span className="stat-label">Used</span>
                  </div>
                  <div className="balance-stat">
                    <span className="stat-value">{balance.pending_days}</span>
                    <span className="stat-label">Pending</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default LeaveRequest
