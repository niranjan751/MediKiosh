// ============================================================
// MEDIKIOSK – Protected Route Guard
// ============================================================
// Wraps authenticated-only routes.
// Redirects unauthenticated users to /login.
// Optionally restricts to specific roles.

import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

/**
 * @param {string[]} [roles] - If provided, user must have one of these roles.
 */
export default function ProtectedRoute({ children, roles }) {
  const { user, loading, isAuthenticated } = useAuth()
  const location = useLocation()

  // While token is being verified against backend, show nothing (avoids flicker)
  if (loading) {
    return (
      <div style={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f8fafc' }}>
        <div style={{ textAlign: 'center', color: '#64748b' }}>
          <div style={{ width: '40px', height: '40px', border: '3px solid #e2e8f0', borderTop: '3px solid #1565c0', borderRadius: '50%', animation: 'spin 0.8s linear infinite', margin: '0 auto 12px' }} />
          <p>Loading…</p>
        </div>
      </div>
    )
  }

  // Not logged in → redirect to login with return path
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  // Role check
  if (roles && !roles.includes(user.role)) {
    return <Navigate to={`/dashboard/${user.role}`} replace />
  }

  return children
}
