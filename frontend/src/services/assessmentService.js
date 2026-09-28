// ============================================================
// MEDIKIOSK – Assessment Service
// ============================================================
// Wraps all /api/assessments/* endpoints (clinical + AYUSH).

import api from './api'

// ── GET /api/assessments ──────────────────────────────────────
export const getAssessments = async () => {
  const { data } = await api.get('/api/assessments')
  return data // { success, count, data: [...] }
}

// ── GET /api/assessments/:id ──────────────────────────────────
export const getAssessment = async (id) => {
  const { data } = await api.get(`/api/assessments/${id}`)
  return data.data
}

// ── POST /api/assessments ─────────────────────────────────────
// Creates a new clinical assessment session
export const createAssessment = async ({ language = 'en', type = 'clinical', consentGiven = false }) => {
  const { data } = await api.post('/api/assessments', { language, type, consentGiven })
  return data.data
}

// ── PUT /api/assessments/:id ──────────────────────────────────
// Update assessment fields (e.g. mark consentGiven = true)
export const updateAssessment = async (id, updates) => {
  const { data } = await api.put(`/api/assessments/${id}`, updates)
  return data.data
}

// ── POST /api/assessments/:id/transcript ─────────────────────
// Append a message to the interview transcript
export const appendTranscript = async (id, { role, message }) => {
  const { data } = await api.post(`/api/assessments/${id}/transcript`, { role, message })
  return data.data
}

// ── POST /api/assessments/ayush/prakriti ─────────────────────
export const submitPrakriti = async (responses) => {
  const { data } = await api.post('/api/assessments/ayush/prakriti', responses)
  return data.data
}

// ── POST /api/assessments/ayush/vikriti ──────────────────────
export const submitVikriti = async (responses) => {
  const { data } = await api.post('/api/assessments/ayush/vikriti', responses)
  return data.data
}

const assessmentService = {
  getAssessments,
  getAssessment,
  createAssessment,
  updateAssessment,
  appendTranscript,
  submitPrakriti,
  submitVikriti,
}
export default assessmentService
