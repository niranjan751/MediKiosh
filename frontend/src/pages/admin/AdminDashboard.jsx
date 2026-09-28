import { Users, Stethoscope, Calendar, Activity, FileText, AlertTriangle, Leaf, UserPlus, FileCheck } from 'lucide-react'

export default function AdminDashboard() {
  const STATS_ROW_1 = [
    { label: 'Patients', value: '1,248', icon: Users, color: 'blue' },
    { label: 'Doctors', value: '86', icon: Stethoscope, color: 'teal' },
    { label: 'Appointments', value: '142', icon: Calendar, color: 'purple' },
    { label: 'Assessments', value: '356', icon: Activity, color: 'amber' },
  ]

  const STATS_ROW_2 = [
    { label: 'Documents', value: '2,438', icon: FileText, color: 'indigo' },
    { label: 'AI Reports', value: '892', icon: FileCheck, color: 'green' },
    { label: 'AI Alerts', value: '24', icon: AlertTriangle, color: 'rose' },
    { label: 'AYUSH', value: '128', icon: Leaf, color: 'emerald' },
  ]

  const RECENT_USERS = [
    { id: 1, name: 'Patient A', role: 'Patient', dept: 'General', status: 'Active' },
    { id: 2, name: 'Dr. Kumar', role: 'Doctor', dept: 'Cardiology', status: 'Active' },
    { id: 3, name: 'Patient B', role: 'Patient', dept: 'General', status: 'Pending' },
  ]

  const ALERTS = [
    { id: 1, type: 'critical', msg: 'Pending doctor verification' },
    { id: 2, type: 'warning', msg: 'AI report requires doctor review' },
    { id: 3, type: 'info', msg: 'New document processing completed' },
  ]

  return (
    <>
      <div className="admin-welcome">
        <h1>Good Morning, Admin <span className="admin-wave">👋</span></h1>
        <p>Manage and monitor the MediKiosk healthcare platform.</p>
      </div>

      {/* Stats Grid 1 */}
      <div className="admin-stats-grid">
        {STATS_ROW_1.map((stat, idx) => (
          <div key={idx} className="admin-stat-card">
            <div className="admin-stat-info">
              <h3>{stat.label}</h3>
              <div className="admin-stat-value">{stat.value}</div>
            </div>
            <div className={`admin-stat-icon bg-${stat.color}`}>
              <stat.icon size={24} />
            </div>
          </div>
        ))}
      </div>

      {/* Stats Grid 2 */}
      <div className="admin-stats-grid">
        {STATS_ROW_2.map((stat, idx) => (
          <div key={idx} className="admin-stat-card">
            <div className="admin-stat-info">
              <h3>{stat.label}</h3>
              <div className="admin-stat-value">{stat.value}</div>
            </div>
            <div className={`admin-stat-icon bg-${stat.color}`}>
              <stat.icon size={24} />
            </div>
          </div>
        ))}
      </div>

      <div className="admin-two-col">
        {/* Platform Activity */}
        <div className="admin-panel">
          <div className="admin-panel-header">
            <h2>Platform Activity</h2>
            <Activity size={18} className="admin-icon-muted" />
          </div>
          <div className="admin-activity-list">
            <div className="admin-activity-item">
              <span>Patients</span>
              <strong>1,248</strong>
            </div>
            <div className="admin-activity-item">
              <span>Doctors</span>
              <strong>86</strong>
            </div>
            <div className="admin-activity-item">
              <span>Documents</span>
              <strong>2,438</strong>
            </div>
            <div className="admin-activity-item">
              <span>Assessments</span>
              <strong>356</strong>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="admin-panel">
          <div className="admin-panel-header">
            <h2>Quick Actions</h2>
          </div>
          <div className="admin-actions-grid">
            <button className="admin-action-btn">
              <UserPlus size={18} /> Add Doctor
            </button>
            <button className="admin-action-btn">
              <UserPlus size={18} /> Add Patient
            </button>
            <button className="admin-action-btn">
              <Calendar size={18} /> View Appointments
            </button>
            <button className="admin-action-btn">
              <AlertTriangle size={18} /> View Alerts
            </button>
          </div>
        </div>
      </div>

      {/* Recent Users */}
      <div className="admin-panel">
        <div className="admin-panel-header">
          <h2>Recent Users</h2>
        </div>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Department</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {RECENT_USERS.map(user => (
                <tr key={user.id}>
                  <td className="admin-fw-600">{user.name}</td>
                  <td>{user.role}</td>
                  <td>{user.dept}</td>
                  <td>
                    <span className={`admin-badge-status status-${user.status.toLowerCase()}`}>
                      {user.status}
                    </span>
                  </td>
                  <td>
                    <button className="admin-btn-sm">View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* System Alerts */}
      <div className="admin-panel">
        <div className="admin-panel-header">
          <h2>System Alerts</h2>
          <AlertTriangle size={18} className="admin-icon-rose" />
        </div>
        <div className="admin-alerts-list">
          {ALERTS.map(alert => (
            <div key={alert.id} className={`admin-alert-item alert-${alert.type}`}>
              <div className="admin-alert-content">
                {alert.type === 'critical' && <AlertTriangle size={16} />}
                {alert.type === 'warning' && <AlertTriangle size={16} />}
                {alert.type === 'info' && <span className="alert-dot"></span>}
                <span>{alert.msg}</span>
              </div>
              <button className="admin-btn-outline-sm">
                {alert.type === 'critical' ? 'Review' : 'View'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </>
  )
}
