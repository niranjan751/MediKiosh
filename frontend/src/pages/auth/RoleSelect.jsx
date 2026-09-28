import { useNavigate } from 'react-router-dom'
import {
  ArrowLeft,
  ArrowRight,
  Building2,
  Heart,
  ShieldCheck,
  Stethoscope,
  User,
} from 'lucide-react'
import './RoleSelect.css'

const ROLES = [
  {
    id: 'patient',
    label: 'Patient',
    tagline: 'Book appointments, view records & AI health intake',
    Icon: User,
    color: 'blue',
    route: '/dashboard/patient',
    features: ['AI Clinical Interview', 'Medical Documents', 'Health Timeline', 'Appointments'],
  },
  {
    id: 'doctor',
    label: 'Doctor',
    tagline: 'Review patient cases, clinical summaries & records',
    Icon: Stethoscope,
    color: 'teal',
    route: '/dashboard/doctor',
    features: ['Patient List', 'Clinical Review', 'SOAP Notes', 'Red-Flag Alerts'],
  },
  {
    id: 'admin',
    label: 'Admin',
    tagline: 'Manage hospital operations, staff & analytics',
    Icon: Building2,
    color: 'purple',
    route: '/dashboard/admin',
    features: ['User Management', 'Analytics', 'Doctor Roster', 'System Settings'],
  },
]

function RoleSelect() {
  const navigate = useNavigate()

  return (
    <main className="rs-bg">
      {/* ── Minimal header ── */}
      <header className="rs-header">
        <a className="rs-brand" href="/">
          <span className="rs-brand-mark" aria-hidden="true">
            <Heart size={17} strokeWidth={2.4} fill="currentColor" />
          </span>
          <strong>MediKiosk</strong>
        </a>
      </header>

      <div className="rs-wrap">
        {/* Back button */}
        <button
          className="rs-back"
          type="button"
          onClick={() => navigate(-1)}
          aria-label="Go back"
        >
          <ArrowLeft size={16} /> Back
        </button>

        {/* Heading */}
        <div className="rs-heading">
          <span className="rs-eyebrow">Step 2 of 2</span>
          <h1>Select your role</h1>
          <p>Choose the portal that matches your access. You can change this later from settings.</p>
        </div>

        {/* Role cards */}
        <div className="rs-grid" role="list">
          {ROLES.map(({ id, label, tagline, Icon, color, route, features }) => (
            <button
              key={id}
              className={`rs-card rs-card--${color}`}
              role="listitem"
              aria-label={`Continue as ${label}`}
              onClick={() => navigate(route)}
            >
              <div className="rs-card-top">
                <span className={`rs-icon rs-icon--${color}`} aria-hidden="true">
                  <Icon size={28} strokeWidth={1.8} />
                </span>
                <div className="rs-card-title">
                  <h2>{label}</h2>
                  <p>{tagline}</p>
                </div>
                <ArrowRight className="rs-card-arrow" size={20} aria-hidden="true" />
              </div>

              <ul className="rs-features" aria-label={`${label} features`}>
                {features.map((f) => (
                  <li key={f}>
                    <span className="rs-dot" aria-hidden="true" />
                    {f}
                  </li>
                ))}
              </ul>
            </button>
          ))}
        </div>

        {/* Security note */}
        <p className="rs-security">
          <ShieldCheck size={13} aria-hidden="true" />
          Access is verified against your account permissions. Unauthorised role access is blocked.
        </p>
      </div>
    </main>
  )
}

export default RoleSelect
