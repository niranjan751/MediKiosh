import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  ArrowRight,
  Building2,
  Eye,
  EyeOff,
  Heart,
  Menu,
  ShieldCheck,
  Stethoscope,
  User,
  X,
} from 'lucide-react'
import { useAuth } from '../../context/AuthContext'
import './Login.css'

const LOGIN_ROLES = [
  { id: 'patient', label: 'Patient', Icon: User },
  { id: 'doctor',  label: 'Doctor',  Icon: Stethoscope },
  { id: 'admin',   label: 'Admin',   Icon: Building2 },
]

const ROLE_ROUTES = {
  patient: '/dashboard/patient',
  doctor:  '/dashboard/doctor',
  admin:   '/dashboard/admin',
}

function LoginNavbar() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="ln-header">
      <nav className="ln-nav" aria-label="Main navigation">
        {/* Brand */}
        <a className="ln-brand" href="/" aria-label="MediKiosk home">
          <span className="ln-brand-mark" aria-hidden="true">
            <Heart size={18} strokeWidth={2.4} fill="currentColor" />
          </span>
          <strong>MediKiosk</strong>
        </a>

        {/* Mobile toggle */}
        <button
          className="ln-menu-toggle"
          type="button"
          aria-label={menuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={menuOpen}
          aria-controls="ln-nav-content"
          onClick={() => setMenuOpen((o) => !o)}
        >
          {menuOpen ? <X size={22} /> : <Menu size={22} />}
        </button>

        {/* Links */}
        <div id="ln-nav-content" className={`ln-nav-content${menuOpen ? ' ln-nav-content--open' : ''}`}>
          <div className="ln-links">
            <a href="/" onClick={() => setMenuOpen(false)}>Home</a>
            <a href="/#features" onClick={() => setMenuOpen(false)}>Features</a>
            <a href="/#how-it-works" onClick={() => setMenuOpen(false)}>How It Works</a>
            <a href="/#about" onClick={() => setMenuOpen(false)}>About</a>
          </div>
          <div className="ln-actions">
            <a className="ln-signin" href="/login">Sign In</a>
            <a className="ln-cta" href="/signup">
              Get Started <ArrowRight size={15} aria-hidden="true" />
            </a>
          </div>
        </div>
      </nav>
    </header>
  )
}

function Login() {
  const navigate = useNavigate()
  const { login, loading } = useAuth()
  const [role,         setRole]         = useState('patient')
  const [showPassword, setShowPassword] = useState(false)
  const [notice,       setNotice]       = useState('')
  const [form,         setForm]         = useState({ email: '', password: '' })

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setNotice('')
    try {
      const user = await login({ email: form.email, password: form.password })
      // Route by role returned from backend (ignores UI role selector for security)
      navigate(ROLE_ROUTES[user.role] || ROLE_ROUTES.patient)
    } catch (err) {
      setNotice(err.message || 'Login failed. Please check your credentials.')
    }
  }

  return (
    <main className="lp-bg">
      {/* ── Top Navbar ── */}
      <LoginNavbar />

      {/* ── Card ── */}
      <section className="lp-card" aria-labelledby="login-heading">
        <div className="lp-card-bar" aria-hidden="true" />
        {/* Back button */}
        <div className="lp-back-row">
          <button className="lp-back-btn" type="button" onClick={() => navigate(-1)}>
            ← Back
          </button>
        </div>

        <div className="lp-card-body">
          {/* Heading */}
          <div className="lp-heading">
            <h1 id="login-heading">Welcome Back</h1>
            <p>Sign in to your MediKiosk account</p>
          </div>

          {/* Role selector */}
          <div className="lp-role-selector" role="group" aria-label="Select your role">
            {LOGIN_ROLES.map(({ id, label, Icon }) => (
              <button
                key={id}
                type="button"
                className={`lp-role-tab${role === id ? ' lp-role-tab--active' : ''}`}
                onClick={() => setRole(id)}
                aria-pressed={role === id}
              >
                <Icon size={14} aria-hidden="true" />
                {label}
              </button>
            ))}
          </div>

          {/* Form */}
          <form className="lp-form" onSubmit={handleSubmit} noValidate>

            {/* Email */}
            <div className="lp-field">
              <label htmlFor="login-email">Email address</label>
              <input
                id="login-email"
                name="email"
                type="email"
                placeholder="Enter your email"
                autoComplete="email"
                value={form.email}
                onChange={set('email')}
                required
              />
            </div>

            {/* Password */}
            <div className="lp-field">
              <label htmlFor="login-password">Password</label>
              <div className="lp-pw-wrap">
                <input
                  id="login-password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  value={form.password}
                  onChange={set('password')}
                  required
                />
                <button
                  type="button"
                  className="lp-pw-toggle"
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                  aria-pressed={showPassword}
                  onClick={() => setShowPassword((v) => !v)}
                >
                  {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                </button>
              </div>
            </div>

            {/* Options row */}
            <div className="lp-options">
              <label className="lp-remember">
                <input type="checkbox" name="remember" />
                <span>Remember me</span>
              </label>
              <a className="lp-forgot" href="#forgot-password">Forgot password?</a>
            </div>

            {/* Submit */}
            <button
              id="login-submit-btn"
              type="submit"
              className={`lp-submit${loading ? ' lp-submit--loading' : ''}`}
              disabled={loading}
            >
              {loading
                ? <span className="lp-spinner" aria-hidden="true" />
                : <>Sign In <ArrowRight size={16} aria-hidden="true" /></>
              }
            </button>

            {/* Notice */}
            {notice && (
              <p className="lp-notice" role="status">{notice}</p>
            )}
          </form>

          {/* Divider */}
          <div className="lp-divider" aria-hidden="true"><span>or</span></div>

          {/* Register */}
          <p className="lp-register">
            Don&apos;t have an account?{' '}
            <a href="/signup">Get Started</a>
          </p>
        </div>

        {/* Security footnote */}
        <footer className="lp-card-footer">
          <ShieldCheck size={13} aria-hidden="true" />
          <span>Your health data is private &amp; encrypted. HIPAA-aligned security.</span>
        </footer>
      </section>

      {/* Page watermark */}
      <p className="lp-watermark" aria-hidden="true">MEDIKIOSK / SECURE ACCESS</p>
    </main>
  )
}

export default Login