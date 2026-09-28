import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  AlertTriangle,
  Calendar,
  Clock,
  FileText,
  Heart,
  LogOut,
  Search,
  Activity,
  Users,
  User
} from 'lucide-react'
import './DoctorDashboard.css'

function DoctorDashboard() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('dashboard')

  const STATS = [
    { label: 'Total Patients', value: '124', icon: Users, color: 'blue' },
    { label: 'Pending Assessments', value: '18', icon: Activity, color: 'purple' },
    { label: 'Medical Documents', value: '32', icon: FileText, color: 'teal' },
    { label: 'Clinical Alerts', value: '5', icon: AlertTriangle, color: 'rose' }
  ]

  const APPOINTMENTS = [
    { time: '09:30 AM', patient: 'Patient A', type: 'Initial Consultation', status: 'Waiting' },
    { time: '10:30 AM', patient: 'Patient B', type: 'Follow-up', status: 'Scheduled' },
    { time: '11:30 AM', patient: 'Patient C', type: 'Review Reports', status: 'Scheduled' },
  ]

  const RECENT_PATIENTS = [
    { id: 1, name: 'Patient A', assessment: 'Completed', docs: 3, status: 'Review' },
    { id: 2, name: 'Patient B', assessment: 'Pending', docs: 2, status: 'New' },
    { id: 3, name: 'Patient C', assessment: 'Completed', docs: 0, status: 'Clear' },
  ]

  const ALERTS = [
    { id: 1, type: 'critical', msg: 'Patient B requires review - Elevated Blood Pressure' },
    { id: 2, type: 'info', msg: 'New medical document uploaded for Patient A' },
  ]

  return (
    <div className="doc-layout">
      {/* Top Navbar */}
      <nav className="doc-navbar">
        <div className="doc-nav-left">
          <div className="doc-brand">
            <span className="doc-brand-icon"><Heart size={20} fill="currentColor" /></span>
            <h2>MediKiosk</h2>
          </div>
          <div className="doc-nav-links">
            <button className={`doc-nav-link ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>Dashboard</button>
            <button className={`doc-nav-link ${activeTab === 'patients' ? 'active' : ''}`} onClick={() => setActiveTab('patients')}>Patients</button>
            <button className={`doc-nav-link ${activeTab === 'assessments' ? 'active' : ''}`} onClick={() => setActiveTab('assessments')}>Assessments</button>
            <button className={`doc-nav-link ${activeTab === 'documents' ? 'active' : ''}`} onClick={() => setActiveTab('documents')}>Documents</button>
          </div>
        </div>
        <div className="doc-nav-right">
          <div className="doc-search">
            <Search size={16} />
            <input type="text" placeholder="Search patients..." />
          </div>
          <button className="doc-logout" onClick={() => navigate('/login')}>
            <LogOut size={18} />
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="doc-main">
        {/* Welcome Header */}
        <header className="doc-welcome">
          <div className="doc-welcome-text">
            <h1>Good Morning, Dr. Kumar <span className="doc-wave">👋</span></h1>
            <p>Here's your clinical overview for today.</p>
          </div>
          <div className="doc-profile">
            <div className="doc-avatar"><User size={24} /></div>
            <div className="doc-profile-info">
              <span className="doc-name">Dr. Kumar</span>
              <span className="doc-dept">General Medicine</span>
            </div>
          </div>
        </header>

        {/* Stats Row */}
        <section className="doc-stats-grid">
          {STATS.map((stat, idx) => (
            <div key={idx} className="doc-stat-card">
              <div className="doc-stat-info">
                <h3>{stat.label}</h3>
                <div className="doc-stat-value">{stat.value}</div>
              </div>
              <div className={`doc-stat-icon bg-${stat.color}`}>
                <stat.icon size={24} />
              </div>
            </div>
          ))}
        </section>

        {/* Two Column Layout: Appointments & Quick Actions */}
        <div className="doc-two-col">
          {/* Appointments */}
          <section className="doc-panel">
            <div className="doc-panel-header">
              <h2>Today's Appointments</h2>
              <Calendar size={20} className="doc-icon-muted" />
            </div>
            <div className="doc-apt-list">
              {APPOINTMENTS.map((apt, idx) => (
                <div key={idx} className="doc-apt-item">
                  <div className="doc-apt-time">
                    <Clock size={16} /> {apt.time}
                  </div>
                  <div className="doc-apt-details">
                    <strong className="doc-apt-name">{apt.patient}</strong>
                    <span className="doc-apt-type">{apt.type}</span>
                  </div>
                  <div className={`doc-apt-status status-${apt.status.toLowerCase()}`}>
                    {apt.status}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Quick Actions */}
          <section className="doc-panel">
            <div className="doc-panel-header">
              <h2>Quick Actions</h2>
            </div>
            <div className="doc-actions-grid">
              <button className="doc-action-btn">
                <Users size={20} /> View Patients
              </button>
              <button className="doc-action-btn">
                <Activity size={20} /> Review Assessments
              </button>
              <button className="doc-action-btn">
                <FileText size={20} /> View Documents
              </button>
              <button className="doc-action-btn btn-alert">
                <AlertTriangle size={20} /> View Alerts
              </button>
            </div>
          </section>
        </div>

        {/* Recent Patients Table */}
        <section className="doc-panel">
          <div className="doc-panel-header">
            <h2>Recent Patients</h2>
          </div>
          <div className="doc-table-wrapper">
            <table className="doc-table">
              <thead>
                <tr>
                  <th>Patient Name</th>
                  <th>Assessment</th>
                  <th>Documents</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {RECENT_PATIENTS.map((p) => (
                  <tr key={p.id}>
                    <td className="doc-fw-600">{p.name}</td>
                    <td>
                      <span className={`badge badge-${p.assessment.toLowerCase()}`}>
                        {p.assessment}
                      </span>
                    </td>
                    <td>{p.docs} {p.docs === 1 ? 'file' : 'files'}</td>
                    <td>
                      <span className={`status-dot status-${p.status.toLowerCase()}`}>
                        {p.status}
                      </span>
                    </td>
                    <td>
                      <button className="doc-btn-sm">View</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Clinical Alerts */}
        <section className="doc-panel">
          <div className="doc-panel-header">
            <h2>Clinical Alerts</h2>
            <AlertTriangle size={20} className="doc-icon-rose" />
          </div>
          <div className="doc-alerts-list">
            {ALERTS.map(alert => (
              <div key={alert.id} className={`doc-alert-item alert-${alert.type}`}>
                <div className="doc-alert-content">
                  <AlertTriangle size={18} />
                  <span>{alert.msg}</span>
                </div>
                <button className="doc-btn-outline-sm">
                  {alert.type === 'critical' ? 'Review' : 'View'}
                </button>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}

export default DoctorDashboard
