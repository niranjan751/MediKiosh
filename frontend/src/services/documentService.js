// ============================================================
// MEDIKIOSK – Document Service
// ============================================================
// Wraps all /api/documents/* endpoints (upload, OCR, list, delete).

import api from './api'

// ── POST /api/documents (multipart file upload) ───────────────
export const uploadDocument = async (file, assessmentId = null) => {
  const formData = new FormData()
  formData.append('document', file)
  if (assessmentId) formData.append('assessmentId', assessmentId)

  const { data } = await api.post('/api/documents', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data.data
}

// ── GET /api/documents (list all documents for the user) ──────
export const getDocuments = async () => {
  const { data } = await api.get('/api/documents')
  return data // { success, count, data: [...] }
}

// ── GET /api/documents/:id ────────────────────────────────────
export const getDocument = async (id) => {
  const { data } = await api.get(`/api/documents/${id}`)
  return data.data
}

// ── GET /api/documents/:id/ocr ────────────────────────────────
// Fetches the OCR result for a document (after AI processing)
export const getOCRResult = async (id) => {
  const { data } = await api.get(`/api/documents/${id}/ocr`)
  return data.data
}

// ── DELETE /api/documents/:id ─────────────────────────────────
export const deleteDocument = async (id) => {
  const { data } = await api.delete(`/api/documents/${id}`)
  return data
}

const documentService = { uploadDocument, getDocuments, getDocument, getOCRResult, deleteDocument }
export default documentService
