// ============================================================
// MEDIKIOSK – Central Axios API Client
// ============================================================
// All HTTP calls go through this single instance so that
// auth tokens, base URL, and error handling are applied once.

import axios from 'axios'

// In dev Vite proxies /api → http://localhost:5000  (see vite.config.js)
// In prod set VITE_API_BASE_URL to the deployed backend URL
const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 15000,
})

// ── Request interceptor: attach JWT from localStorage ─────────
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('mk_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// ── Response interceptor: global 401 handling ─────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired / invalid – clear local session
      localStorage.removeItem('mk_token')
      localStorage.removeItem('mk_user')
      // Only redirect if not already on auth pages
      const onAuthPage = ['/login', '/signup', '/'].includes(window.location.pathname)
      if (!onAuthPage) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  },
)

export default api
