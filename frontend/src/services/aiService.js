// ============================================================
// MEDIKIOSK – AI Service Client
// ============================================================
// Calls the Python FastAPI AI microservice (port 8000).
// Vite proxies /ai-api → http://localhost:8000 in dev.

import axios from 'axios'

const AI_BASE = import.meta.env.VITE_AI_SERVICE_URL || ''

const aiApi = axios.create({
  baseURL: AI_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000, // AI calls can be slow
})

// ── CLINICAL INTERVIEW (SOCRATES) ─────────────────────────────

// Start a new adaptive interview session
export const startInterview = async ({ language = 'en', chief_complaint = null }) => {
  const { data } = await aiApi.post('/ai-api/interview/start', { language, chief_complaint })
  return data
}

// Get current question for a session
export const getInterviewQuestion = async (sessionId) => {
  const { data } = await aiApi.get(`/ai-api/interview/${sessionId}/question`)
  return data
}

// Submit patient answer
export const submitAnswer = async ({ session_id, question_id, answer }) => {
  const { data } = await aiApi.post('/ai-api/interview/answer', { session_id, question_id, answer })
  return data
}

// Get interview progress
export const getInterviewProgress = async (sessionId) => {
  const { data } = await aiApi.get(`/ai-api/interview/${sessionId}/progress`)
  return data
}

// Get all collected answers
export const getInterviewAnswers = async (sessionId) => {
  const { data } = await aiApi.get(`/ai-api/interview/${sessionId}/answers`)
  return data
}

// ── RED FLAGS ─────────────────────────────────────────────────

// Check symptoms for red flags
export const detectRedFlags = async ({ symptoms = [], clinical_text = '', interview_answers = {}, language = 'en' }) => {
  const { data } = await aiApi.post('/ai-api/red-flags/detect', {
    symptoms,
    clinical_text,
    interview_answers,
    language,
  })
  return data
}

// ── CLINICAL SUMMARY ──────────────────────────────────────────

// Generate AI clinical summary from interview + documents
export const generateClinicalSummary = async ({
  patient_id,
  session_id,
  patient_info,
  interview_data,
  documents_data = [],
  clinical_mode = 'standard',
  ayush_data = null,
}) => {
  const { data } = await aiApi.post('/ai-api/summary/generate', {
    patient_id,
    session_id,
    patient_info,
    interview_data,
    documents_data,
    clinical_mode,
    ayush_data,
  })
  return data
}

// Doctor review of AI summary
export const reviewSummary = async ({ summary, comments, doctor_name, confirmed_diagnoses, prescribed_plan }) => {
  const { data } = await aiApi.post('/ai-api/summary/review', {
    summary,
    comments,
    doctor_name,
    confirmed_diagnoses,
    prescribed_plan,
  })
  return data
}

// ── OCR ───────────────────────────────────────────────────────

// Process a document through OCR (send as FormData with file)
export const processOCR = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await aiApi.post('/ai-api/ocr/process', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

// ── AYUSH ─────────────────────────────────────────────────────

export const getAyushAssessment = async ({ patient_id, responses }) => {
  const { data } = await aiApi.post('/ai-api/ayush/assess', { patient_id, responses })
  return data
}

// ── HEALTH CHECK ──────────────────────────────────────────────
export const checkAIHealth = async () => {
  const { data } = await aiApi.get('/ai-api/health')
  return data
}

const aiService = {
  startInterview,
  getInterviewQuestion,
  submitAnswer,
  getInterviewProgress,
  getInterviewAnswers,
  detectRedFlags,
  generateClinicalSummary,
  reviewSummary,
  processOCR,
  getAyushAssessment,
  checkAIHealth,
}
export default aiService
