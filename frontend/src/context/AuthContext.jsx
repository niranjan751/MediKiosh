// ============================================================
// MEDIKIOSK – Auth Context
// ============================================================
// Provides authentication state (user, token, loading) to the
// entire app. Wrap <AppRoutes> with <AuthProvider>.

import { createContext, useContext, useEffect, useState, useCallback } from 'react'
import authService from '../services/authService'

// ── Context ───────────────────────────────────────────────────
const AuthContext = createContext(null)

// ── Provider ──────────────────────────────────────────────────
export function AuthProvider({ children }) {
  const [user,    setUser]    = useState(() => authService.getCachedUser())
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState(null)

  // On mount: verify token against backend, keep session fresh
  useEffect(() => {
    const token = authService.getToken()
    if (!token) {
      setLoading(false)
      return
    }

    authService.getMe()
      .then((freshUser) => setUser(freshUser))
      .catch(() => {
        // Token invalid / expired → clear stale session
        authService.clearSession()
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [])

  // ── login ──────────────────────────────────────────────────
  const login = useCallback(async (credentials) => {
    setError(null)
    setLoading(true)
    try {
      const result = await authService.login(credentials)
      setUser(result.user)
      return result.user
    } catch (err) {
      const msg = err.response?.data?.message || 'Login failed. Please try again.'
      setError(msg)
      throw new Error(msg)
    } finally {
      setLoading(false)
    }
  }, [])

  // ── register ───────────────────────────────────────────────
  const register = useCallback(async (userData) => {
    setError(null)
    setLoading(true)
    try {
      const result = await authService.register(userData)
      setUser(result.user)
      return result.user
    } catch (err) {
      const msg = err.response?.data?.message || 'Registration failed. Please try again.'
      setError(msg)
      throw new Error(msg)
    } finally {
      setLoading(false)
    }
  }, [])

  // ── logout ─────────────────────────────────────────────────
  const logout = useCallback(async () => {
    setLoading(true)
    try {
      await authService.logout()
    } finally {
      setUser(null)
      setLoading(false)
    }
  }, [])

  // ── clearError ────────────────────────────────────────────
  const clearError = useCallback(() => setError(null), [])

  const value = {
    user,          // null | { _id, name, email, role }
    loading,       // true during async auth operations
    error,         // string | null
    isAuthenticated: !!user,
    isPatient: user?.role === 'patient',
    isDoctor:  user?.role === 'doctor',
    isAdmin:   user?.role === 'admin',
    login,
    register,
    logout,
    clearError,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// ── useAuth hook ──────────────────────────────────────────────
export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used inside <AuthProvider>')
  }
  return ctx
}

export default AuthContext
