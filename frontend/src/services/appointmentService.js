// ============================================================
// MEDIKIOSK – Appointment Service
// ============================================================
// Wraps all /api/appointments/* endpoints.

import api from './api'

// ── GET /api/appointments ─────────────────────────────────────
export const getAppointments = async () => {
  const { data } = await api.get('/api/appointments')
  return data // { success, count, data: [...] }
}

// ── GET /api/appointments/:id ─────────────────────────────────
export const getAppointment = async (id) => {
  const { data } = await api.get(`/api/appointments/${id}`)
  return data.data
}

// ── POST /api/appointments ────────────────────────────────────
export const createAppointment = async ({ doctor, date, timeSlot, reason }) => {
  const { data } = await api.post('/api/appointments', { doctor, date, timeSlot, reason })
  return data.data
}

// ── PUT /api/appointments/:id ─────────────────────────────────
export const updateAppointment = async (id, updates) => {
  const { data } = await api.put(`/api/appointments/${id}`, updates)
  return data.data
}

// ── DELETE /api/appointments/:id (cancel) ─────────────────────
export const cancelAppointment = async (id) => {
  const { data } = await api.delete(`/api/appointments/${id}`)
  return data.data
}

const appointmentService = { getAppointments, getAppointment, createAppointment, updateAppointment, cancelAppointment }
export default appointmentService
