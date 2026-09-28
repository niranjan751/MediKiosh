// ============================================================
// MEDIKIOSK – Patient Service
// ============================================================
// Wraps all /api/patients/* endpoints.

import api from './api'

// ── GET /api/patients (admin / doctor: all patients) ──────────
export const getPatients = async () => {
  const { data } = await api.get('/api/patients')
  return data // { success, count, data: [...] }
}

// ── GET /api/patients/me (logged-in patient's own profile) ────
export const getMyProfile = async () => {
  const { data } = await api.get('/api/patients/me')
  return data.data
}

// ── GET /api/patients/:id ─────────────────────────────────────
export const getPatient = async (id) => {
  const { data } = await api.get(`/api/patients/${id}`)
  return data.data
}

// ── POST /api/patients ─────────────────────────────────────────
export const createPatient = async (profileData) => {
  const { data } = await api.post('/api/patients', profileData)
  return data.data
}

// ── PUT /api/patients/:id ─────────────────────────────────────
export const updatePatient = async (id, updates) => {
  const { data } = await api.put(`/api/patients/${id}`, updates)
  return data.data
}

// ── DELETE /api/patients/:id ──────────────────────────────────
export const deletePatient = async (id) => {
  const { data } = await api.delete(`/api/patients/${id}`)
  return data
}

const patientService = { getPatients, getMyProfile, getPatient, createPatient, updatePatient, deletePatient }
export default patientService
