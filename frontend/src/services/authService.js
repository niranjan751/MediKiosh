// ============================================================
// MEDIKIOSK – Auth Service
// ============================================================
// Wraps all /api/auth/* endpoints and manages token storage.

import api from './api'

const TOKEN_KEY = 'mk_token'
const USER_KEY  = 'mk_user'

// ── Save token + user to localStorage ─────────────────────────
const persistSession = ({ token, user }) => {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

// ── Clear session ──────────────────────────────────────────────
export const clearSession = () => {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

// ── Read cached user (no network) ─────────────────────────────
export const getCachedUser = () => {
  try {
    const raw = localStorage.getItem(USER_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export const getToken = () => localStorage.getItem(TOKEN_KEY)

// ── POST /api/auth/register ───────────────────────────────────
export const register = async ({ name, email, password, role = 'patient' }) => {
  const { data } = await api.post('/api/auth/register', { name, email, password, role })
  persistSession(data)
  return data
}

// ── POST /api/auth/login ──────────────────────────────────────
export const login = async ({ email, password }) => {
  const { data } = await api.post('/api/auth/login', { email, password })
  persistSession(data)
  return data
}

// ── GET /api/auth/me ──────────────────────────────────────────
export const getMe = async () => {
  const { data } = await api.get('/api/auth/me')
  // Keep local copy fresh
  localStorage.setItem(USER_KEY, JSON.stringify(data.user))
  return data.user
}

// ── POST /api/auth/logout ─────────────────────────────────────
export const logout = async () => {
  try {
    await api.post('/api/auth/logout')
  } finally {
    clearSession()
  }
}

const authService = { register, login, getMe, logout, getCachedUser, getToken, clearSession }
export default authService
