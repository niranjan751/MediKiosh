import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  ArrowRight,
  CheckCircle2,
  Eye,
  EyeOff,
  Heart,
  Lock,
  Mail,
  Menu,
  ShieldCheck,
  Stethoscope,
  User,
  X,
} from 'lucide-react'
import { useAuth } from '../../context/AuthContext'
import './Signup.css'

const SIGNUP_ROLES = [
  { id: 'patient', label: 'Patient', Icon: User,        desc: 'Book appointments & manage health' },
  { id: 'doctor',  label: 'Doctor',  Icon: Stethoscope, desc: 'Requires hospital verification'    },
]

/* ── Navbar (reused from Login pattern) ── */
function SignupNavbar() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="sn-header">
      <nav className="sn-nav" aria-label="Main navigation">
        <a className="sn-brand" href="/" aria-label="MediKiosk home">
          <span className="sn-brand-mark" aria-hidden="true">
            <Heart size={18} strokeWidth={2.4} fill="currentColor" />
          </span>
          <strong>MediKiosk</strong>
        </a>

        <button
          className="sn-menu-toggle"
          type="button"
          aria-label={menuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={menuOpen}
          aria-controls="sn-nav-content"
          onClick={() => setMenuOpen((o) => !o)}
        >
          {menuOpen ? <X size={22} /> : <Menu size={22} />}
        </button>

        <div
          id="sn-nav-content"
          className={`sn-nav-content${menuOpen ? ' sn-nav-content--open' : ''}`}
        >
          <div className="sn-links">
            <a href="/"            onClick={() => setMenuOpen(false)}>Home</a>
            <a href="/#features"  onClick={() => setMenuOpen(false)}>Features</a>
            <a href="/#how-it-works" onClick={() => setMenuOpen(false)}>How It Works</a>
            <a href="/#about"     onClick={() => setMenuOpen(false)}>About</a>
          </div>
          <div className="sn-actions">
            <a className="sn-login-link" href="/login">Sign In</a>
            <a className="sn-cta" href="/signup">
              Get Started <ArrowRight size={15} aria-hidden="true" />
            </a>
          </div>
        </div>
      </nav>
    </header>
  )
}

/* ── Password strength meter ── */
function strengthScore(pw) {
  let score = 0
  if (pw.length >= 8)            score++
  if (/[A-Z]/.test(pw))         score++
  if (/[0-9]/.test(pw))         score++
  if (/[^A-Za-z0-9]/.test(pw))  score++
  return score          // 0–4
}
const STRENGTH_LABEL = ['', 'Weak', 'Fair', 'Good', 'Strong']
const STRENGTH_COLOR = ['', '#ef4444', '#f97316', '#eab308', '#22c55e']

function PasswordStrength({ password }) {
  if (!password) return null
  const score = strengthScore(password)
  return (
    <div className="sp-strength" aria-live="polite">
      <div className="sp-strength-bars">
        {[1, 2, 3, 4].map((i) => (
          <span
            key={i}
            className="sp-strength-bar"
            style={{ background: i <= score ? STRENGTH_COLOR[score] : '#e5e7eb' }}
          />
        ))}
      </div>
      <span className="sp-strength-label" style={{ color: STRENGTH_COLOR[score] }}>
        {STRENGTH_LABEL[score]}
      </span>
    </div>
  )
}

/* ── Main Signup component ── */
function Signup() {
  const navigate = useNavigate()
  const { register, loading } = useAuth()
  const [role,                setRole]                = useState('patient')
  const [showPassword,        setShowPassword]        = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [success,             setSuccess]             = useState(false)
  const [errors,              setErrors]              = useState({})
  const [serverError,         setServerError]         = useState('')

  const [form, setForm] = useState({
    fullName:        '',
    email:           '',
    password:        '',
    confirmPassword: '',
    terms:           false,
  })

  const set = (field) => (e) =>
    setForm((f) => ({ ...f, [field]: e.target.type === 'checkbox' ? e.target.checked : e.target.value }))

  /* Client-side validation */
  const validate = () => {
    const errs = {}
    if (!form.fullName.trim())                            errs.fullName        = 'Full name is required.'
    if (!form.email.includes('@'))                        errs.email           = 'Enter a valid email address.'
    if (form.password.length < 8)                         errs.password        = 'Password must be at least 8 characters.'
    if (form.password !== form.confirmPassword)           errs.confirmPassword = 'Passwords do not match.'
    if (!form.terms)                                      errs.terms           = 'You must accept the terms to continue.'
    return errs
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const errs = validate()
    setErrors(errs)
    setServerError('')
    if (Object.keys(errs).length) return

    try {
      await register({ name: form.fullName, email: form.email, password: form.password, role })
      setSuccess(true)
      // Auto-redirect to login after showing success
      setTimeout(() => navigate('/login'), 1800)
    } catch (err) {
      setServerError(err.message || 'Registration failed. Please try again.')
    }
  }

  if (success) {
    return (
      <main className="sp-bg">
        <SignupNavbar />
        <div className="sp-success-wrap">
          <div className="sp-success-card">
            <span className="sp-success-icon"><CheckCircle2 size={48} strokeWidth={1.8} /></span>
            <h1>Account created!</h1>
            <p>Welcome to MediKiosk. Your account is ready — please sign in to continue.</p>
            <button className="sp-success-btn" onClick={() => navigate('/login')}>
              Go to Sign In <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </main>
    )
  }

  return (
    <main className="sp-bg">
      <SignupNavbar />

      {/* ── Card ── */}
      <section className="sp-card" aria-labelledby="signup-heading">
        <div className="sp-card-bar" aria-hidden="true" />
        {/* Back button */}
        <div className="lp-back-row">
          <button className="lp-back-btn" type="button" onClick={() => navigate(-1)}>
            ← Back
          </button>
        </div>

        <div className="sp-card-body">
          {/* Heading */}
          <div className="sp-heading">
            <h1 id="signup-heading">Create Account</h1>
            <p>Join MediKiosk — your AI-powered health companion</p>
          </div>

          {/* Role selector */}
          <div className="sp-role-selector" role="group" aria-label="I am signing up as">
            <p className="sp-role-label">I am signing up as</p>
            <div className="sp-role-tabs">
              {SIGNUP_ROLES.map(({ id, label, Icon, desc }) => (
                <button
                  key={id}
                  type="button"
                  className={`sp-role-tab${role === id ? ' sp-role-tab--active' : ''}`}
                  onClick={() => setRole(id)}
                  aria-pressed={role === id}
                >
                  <span className="sp-role-tab-top">
                    <Icon size={15} aria-hidden="true" />
                    <strong>{label}</strong>
                  </span>
                  <span className="sp-role-tab-desc">{desc}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Form */}
          <form className="sp-form" onSubmit={handleSubmit} noValidate>

            {/* Full Name */}
            <div className={`sp-field${errors.fullName ? ' sp-field--error' : ''}`}>
              <label htmlFor="signup-name">Full Name</label>
              <div className="sp-input-wrap">
                <span className="sp-input-icon" aria-hidden="true"><User size={16} /></span>
                <input
                  id="signup-name"
                  name="fullName"
                  type="text"
                  placeholder="Enter your full name"
                  autoComplete="name"
                  value={form.fullName}
                  onChange={set('fullName')}
                  aria-describedby={errors.fullName ? 'err-name' : undefined}
                  required
                />
              </div>
              {errors.fullName && <span id="err-name" className="sp-error-msg" role="alert">{errors.fullName}</span>}
            </div>

            {/* Email */}
            <div className={`sp-field${errors.email ? ' sp-field--error' : ''}`}>
              <label htmlFor="signup-email">Email Address</label>
              <div className="sp-input-wrap">
                <span className="sp-input-icon" aria-hidden="true"><Mail size={16} /></span>
                <input
                  id="signup-email"
                  name="email"
                  type="email"
                  placeholder="you@example.com"
                  autoComplete="email"
                  value={form.email}
                  onChange={set('email')}
                  aria-describedby={errors.email ? 'err-email' : undefined}
                  required
                />
              </div>
              {errors.email && <span id="err-email" className="sp-error-msg" role="alert">{errors.email}</span>}
            </div>

            {/* Password */}
            <div className={`sp-field${errors.password ? ' sp-field--error' : ''}`}>
              <label htmlFor="signup-password">Password</label>
              <div className="sp-input-wrap sp-input-wrap--pw">
                <span className="sp-input-icon" aria-hidden="true"><Lock size={16} /></span>
                <input
                  id="signup-password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Min. 8 characters"
                  autoComplete="new-password"
                  value={form.password}
                  onChange={set('password')}
                  aria-describedby={errors.password ? 'err-pw' : undefined}
                  required
                />
                <button
                  type="button"
                  className="sp-pw-toggle"
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                  onClick={() => setShowPassword((v) => !v)}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              <PasswordStrength password={form.password} />
              {errors.password && <span id="err-pw" className="sp-error-msg" role="alert">{errors.password}</span>}
            </div>

            {/* Confirm Password */}
            <div className={`sp-field${errors.confirmPassword ? ' sp-field--error' : ''}`}>
              <label htmlFor="signup-confirm">Confirm Password</label>
              <div className="sp-input-wrap sp-input-wrap--pw">
                <span className="sp-input-icon" aria-hidden="true"><Lock size={16} /></span>
                <input
                  id="signup-confirm"
                  name="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  placeholder="Re-enter your password"
                  autoComplete="new-password"
                  value={form.confirmPassword}
                  onChange={set('confirmPassword')}
                  aria-describedby={errors.confirmPassword ? 'err-confirm' : undefined}
                  required
                />
                <button
                  type="button"
                  className="sp-pw-toggle"
                  aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                  onClick={() => setShowConfirmPassword((v) => !v)}
                >
                  {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              {errors.confirmPassword && <span id="err-confirm" className="sp-error-msg" role="alert">{errors.confirmPassword}</span>}
            </div>

            {/* Terms */}
            <div className={`sp-terms-wrap${errors.terms ? ' sp-terms-wrap--error' : ''}`}>
              <label className="sp-terms-label">
                <input
                  id="signup-terms"
                  type="checkbox"
                  name="terms"
                  checked={form.terms}
                  onChange={set('terms')}
                  aria-describedby={errors.terms ? 'err-terms' : undefined}
                />
                <span>
                  I agree to the{' '}
                  <a href="#terms" target="_blank" rel="noopener noreferrer">Terms of Service</a>
                  {' '}and{' '}
                  <a href="#privacy" target="_blank" rel="noopener noreferrer">Privacy Policy</a>
                </span>
              </label>
              {errors.terms && <span id="err-terms" className="sp-error-msg" role="alert">{errors.terms}</span>}
            </div>

            {/* Submit */}
            <button
              id="signup-submit-btn"
              type="submit"
              className={`sp-submit${loading ? ' sp-submit--loading' : ''}`}
              disabled={loading}
            >
              {loading
                ? <span className="sp-spinner" aria-hidden="true" />
                : <>Create Account <ArrowRight size={16} aria-hidden="true" /></>
              }
            </button>

            {/* Server error */}
            {serverError && (
              <p className="sp-error-msg" role="alert" style={{ textAlign: 'center', marginTop: '8px' }}>{serverError}</p>
            )}
          </form>

          {/* Divider */}
          <div className="sp-divider" aria-hidden="true"><span>or</span></div>

          {/* Login link */}
          <p className="sp-login-link">
            Already have an account?{' '}
            <a href="/login">Sign In</a>
          </p>
        </div>

        {/* Footer */}
        <footer className="sp-card-footer">
          <ShieldCheck size={13} aria-hidden="true" />
          <span>
            Your role is assigned securely by MediKiosk.
            Public accounts are registered as <strong>Patient</strong> by default.
          </span>
        </footer>
      </section>

      <p className="sp-watermark" aria-hidden="true">MEDIKIOSK / CREATE ACCOUNT</p>
    </main>
  )
}

export default Signup
