'use strict'

const path     = require('path')
const fs       = require('fs')
const Document = require('../models/Document')
const Patient  = require('../models/Patient')

// ── POST /api/documents ───────────────────────────────────────
exports.uploadDocument = async (req, res, next) => {
  try {
    if (!req.file) return res.status(400).json({ success: false, message: 'No file uploaded' })

    const patient = await Patient.findOne({ user: req.user._id })
    if (!patient) return res.status(400).json({ success: false, message: 'Patient profile not found' })

    const doc = await Document.create({
      patient     : patient._id,
      assessment  : req.body.assessmentId || undefined,
      originalName: req.file.originalname,
      fileName    : req.file.filename,
      filePath    : `/uploads/${req.file.filename}`,
      mimeType    : req.file.mimetype,
      fileSize    : req.file.size,
      ocrStatus   : 'pending',
    })

    res.status(201).json({ success: true, data: doc })
  } catch (err) { next(err) }
}

// ── GET /api/documents ────────────────────────────────────────
exports.getDocuments = async (req, res, next) => {
  try {
    let query = {}
    if (req.user.role === 'patient') {
      const patient = await Patient.findOne({ user: req.user._id })
      if (patient) query.patient = patient._id
    }
    const docs = await Document.find(query)
      .populate({ path: 'patient', populate: { path: 'user', select: 'name' } })
      .sort({ createdAt: -1 })
    res.json({ success: true, count: docs.length, data: docs })
  } catch (err) { next(err) }
}

// ── GET /api/documents/:id ────────────────────────────────────
exports.getDocument = async (req, res, next) => {
  try {
    const doc = await Document.findById(req.params.id)
      .populate({ path: 'patient', populate: { path: 'user', select: 'name' } })
    if (!doc) return res.status(404).json({ success: false, message: 'Document not found' })
    res.json({ success: true, data: doc })
  } catch (err) { next(err) }
}

// ── GET /api/documents/:id/ocr ────────────────────────────────
exports.getOCRResult = async (req, res, next) => {
  try {
    const doc = await Document.findById(req.params.id).select('ocrStatus ocrResult processedAt')
    if (!doc) return res.status(404).json({ success: false, message: 'Document not found' })
    res.json({ success: true, data: { ocrStatus: doc.ocrStatus, ocrResult: doc.ocrResult, processedAt: doc.processedAt } })
  } catch (err) { next(err) }
}

// ── DELETE /api/documents/:id ─────────────────────────────────
exports.deleteDocument = async (req, res, next) => {
  try {
    const doc = await Document.findByIdAndDelete(req.params.id)
    if (!doc) return res.status(404).json({ success: false, message: 'Document not found' })

    // Remove physical file
    const fullPath = path.join(__dirname, '..', 'uploads', doc.fileName)
    if (fs.existsSync(fullPath)) fs.unlinkSync(fullPath)

    res.json({ success: true, message: 'Document deleted' })
  } catch (err) { next(err) }
}
