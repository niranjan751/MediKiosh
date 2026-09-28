import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Activity,
  Bell,
  Calendar,
  ChevronDown,
  FileText,
  Heart,
  Home,
  LogOut,
  Mic,
  Settings,
  Stethoscope,
  Upload,
  User,
} from 'lucide-react'
import { useAuth } from '../../context/AuthContext'
import documentService from '../../services/documentService'
import assessmentService from '../../services/assessmentService'
import appointmentService from '../../services/appointmentService'
import './PatientDashboard.css'

const SIDEBAR_LINKS = [
  { id: 'dashboard', label: 'Dashboard', Icon: Home },
  { id: 'assessment', label: 'Assessment', Icon: Mic },
  { id: 'documents', label: 'Documents', Icon: Upload },
  { id: 'history', label: 'Medical History', Icon: Activity },
  { id: 'appointments', label: 'Appointments', Icon: Calendar },
  { id: 'notifications', label: 'Notifications', Icon: Bell },
  { id: 'profile', label: 'Profile', Icon: User },
  { id: 'settings', label: 'Settings', Icon: Settings },
]

const STATS = [
  { label: 'Assessment', value: '0/1', sub: 'Required' },
  { label: 'Documents', value: '0', sub: 'Uploaded' },
  { label: 'History', value: 'View', sub: 'Timeline' },
]

const MAIN_CARDS = [
  { id: 'assessment', label: 'Start Assessment', desc: 'AI clinical interview (Voice + Touch)', Icon: Mic, color: 'blue', route: '/assessment' },
  { id: 'documents', label: 'My Documents', desc: 'Upload prescriptions & lab reports', Icon: Upload, color: 'teal', route: '/documents' },
  { id: 'history', label: 'Medical History', desc: 'View previous assessments & timeline', Icon: Activity, color: 'purple', route: '/history' },
  { id: 'summary', label: 'AI Summary', desc: 'View generated clinical summary', Icon: FileText, color: 'amber', route: '/summary' },
  { id: 'appointments', label: 'Appointments', desc: 'Upcoming consultation status', Icon: Calendar, color: 'green', route: '/appointments' },
  { id: 'alerts', label: 'Health Alerts', desc: 'Priority alerts & notifications', Icon: Bell, color: 'rose', route: '/alerts' },
]

function PatientDashboard() {
  const navigate  = useNavigate()
  const { user, logout } = useAuth()
  const [activeTab,     setActiveTab]     = useState('dashboard')
  const [stats,         setStats]         = useState({ docs: 0, assessments: 0, appointments: 0 })

  // Fetch real counts once on mount
  useEffect(() => {
    Promise.allSettled([
      documentService.getDocuments(),
      assessmentService.getAssessments(),
      appointmentService.getAppointments(),
    ]).then(([docs, assess, appts]) => {
      setStats({
        docs:         docs.status         === 'fulfilled' ? docs.value.count         : 0,
        assessments:  assess.status       === 'fulfilled' ? assess.value.count       : 0,
        appointments: appts.status        === 'fulfilled' ? appts.value.count        : 0,
      })
    })
  }, [])

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  const firstName = user?.name?.split(' ')[0] || 'Patient'

  const dynamicStats = [
    { label: 'Assessments', value: stats.assessments.toString(), sub: 'Completed' },
    { label: 'Documents',   value: stats.docs.toString(),        sub: 'Uploaded' },
    { label: 'Appointments', value: stats.appointments.toString(), sub: 'Scheduled' },
  ]

  return (
    <div className="pd-layout">
      {/* Sidebar */}
      <aside className="pd-sidebar">
        <div className="pd-sidebar-header">
          <div className="pd-brand">
            <span className="pd-brand-icon"><Heart size={20} fill="currentColor" /></span>
            <h2>MediKiosk</h2>
          </div>
        </div>
        
        <nav className="pd-nav">
          {SIDEBAR_LINKS.map(({ id, label, Icon }) => (
            <button
              key={id}
              className={`pd-nav-link ${activeTab === id ? 'pd-nav-link--active' : ''}`}
              onClick={() => setActiveTab(id)}
            >
              <Icon size={20} />
              <span>{label}</span>
            </button>
          ))}
        </nav>

        <div className="pd-sidebar-footer">
          <button className="pd-logout-btn" onClick={handleLogout}>
            <LogOut size={18} />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="pd-main">
        {/* Top Header */}
        <header className="pd-header">
          <div className="pd-header-search">
            {/* Future search bar location */}
          </div>
          <div className="pd-header-actions">
            <button className="pd-icon-btn">
              <Bell size={22} />
              <span className="pd-badge">1</span>
            </button>
            <div className="pd-user-profile">
              <div className="pd-avatar">
                <User size={20} />
              </div>
              <span className="pd-user-name">{firstName}</span>
              <ChevronDown size={16} className="pd-user-chevron" />
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <div className="pd-content">
          <div className="pd-welcome">
            <h1>Good Morning, {firstName} <span className="pd-wave">👋</span></h1>
            <p>Let's complete your health assessment.</p>
          </div>

          {/* Hero Action Card */}
          <section className="pd-hero-card">
            <div className="pd-hero-content">
              <div className="pd-hero-icon-wrapper">
                <Stethoscope size={36} />
              </div>
              <div className="pd-hero-text">
                <h2>Start Health Assessment</h2>
                <p>AI-guided clinical history with Voice + Touch interaction</p>
              </div>
            </div>
            <button className="pd-btn-primary" onClick={() => navigate('/assessment')}>
              Start Assessment
            </button>
          </section>

          {/* Stats Row */}
          <section className="pd-stats">
            {dynamicStats.map(({ label, value, sub }, i) => (
              <div className="pd-stat-box" key={i}>
                <h3>{label}</h3>
                <div className="pd-stat-value">{value}</div>
                <div className="pd-stat-sub">{sub}</div>
              </div>
            ))}
          </section>

          {/* Upcoming Appointment */}
          <section className="pd-appointment-card">
            <div className="pd-apt-header">
              <h3>Upcoming Appointment</h3>
            </div>
            <div className="pd-apt-body">
              <div className="pd-apt-empty">
                <Calendar size={36} />
                <p>No appointment scheduled</p>
              </div>
              <button className="pd-btn-secondary" onClick={() => navigate('/appointments')}>
                Book Appointment
              </button>
            </div>
          </section>

          {/* 6 Main Cards Grid */}
          <h2 className="pd-section-title">Quick Access</h2>
          <section className="pd-grid">
            {MAIN_CARDS.map(({ id, label, desc, Icon, color, route }) => (
              <div key={id} className={`pd-card pd-card--${color}`} onClick={() => navigate(route)}>
                <div className={`pd-card-icon pd-card-icon--${color}`}>
                  <Icon size={28} />
                </div>
                <div className="pd-card-info">
                  <h3>{label}</h3>
                  <p>{desc}</p>
                </div>
              </div>
            ))}
          </section>

        </div>
      </main>
    </div>
  )
}

export default PatientDashboard
