'use strict'

const Assessment = require('../models/Assessment')
const Patient    = require('../models/Patient')

// ── GET /api/assessments ──────────────────────────────────────
exports.getAssessments = async (req, res, next) => {
  try {
    let query = {}
    if (req.user.role === 'patient') {
      const patient = await Patient.findOne({ user: req.user._id })
      if (patient) query.patient = patient._id
    }
    const assessments = await Assessment.find(query)
      .populate({ path: 'patient', populate: { path: 'user', select: 'name email' } })
      .sort({ createdAt: -1 })
    res.json({ success: true, count: assessments.length, data: assessments })
  } catch (err) { next(err) }
}

// ── GET /api/assessments/:id ──────────────────────────────────
exports.getAssessment = async (req, res, next) => {
  try {
    const assessment = await Assessment.findById(req.params.id)
      .populate({ path: 'patient', populate: { path: 'user', select: 'name email' } })
      .populate({ path: 'doctor',  populate: { path: 'user', select: 'name' } })
    if (!assessment) return res.status(404).json({ success: false, message: 'Assessment not found' })
    res.json({ success: true, data: assessment })
  } catch (err) { next(err) }
}

// ── POST /api/assessments ─────────────────────────────────────
exports.createAssessment = async (req, res, next) => {
  try {
    const patient = await Patient.findOne({ user: req.user._id })
    if (!patient) return res.status(400).json({ success: false, message: 'Patient profile not found' })

    const { language, type, consentGiven } = req.body
    const assessment = await Assessment.create({
      patient: patient._id,
      language: language || 'en',
      type: type || 'clinical',
      consentGiven: consentGiven || false,
    })
    res.status(201).json({ success: true, data: assessment })
  } catch (err) { next(err) }
}

// ── PUT /api/assessments/:id ──────────────────────────────────
exports.updateAssessment = async (req, res, next) => {
  try {
    const assessment = await Assessment.findByIdAndUpdate(req.params.id, req.body, {
      new: true, runValidators: true,
    })
    if (!assessment) return res.status(404).json({ success: false, message: 'Assessment not found' })
    res.json({ success: true, data: assessment })
  } catch (err) { next(err) }
}

// ── POST /api/assessments/:id/transcript ─────────────────────
// Append an AI or patient message to the interview transcript
exports.appendTranscript = async (req, res, next) => {
  try {
    const { role, message } = req.body
    if (!role || !message)
      return res.status(400).json({ success: false, message: 'role and message are required' })

    const assessment = await Assessment.findByIdAndUpdate(
      req.params.id,
      { $push: { interviewTranscript: { role, message } } },
      { new: true },
    )
    if (!assessment) return res.status(404).json({ success: false, message: 'Assessment not found' })
    res.json({ success: true, data: assessment })
  } catch (err) { next(err) }
}

// ── POST /api/assessments/ayush/prakriti ─────────────────────
exports.prakritiAssessment = async (req, res, next) => {
  try {
    const patient = await Patient.findOne({ user: req.user._id })
    if (!patient) return res.status(400).json({ success: false, message: 'Patient profile not found' })

    const assessment = await Assessment.create({
      patient: patient._id,
      type   : 'ayush',
      'ayush.prakriti': req.body,
      status : 'completed',
    })
    res.status(201).json({ success: true, data: assessment })
  } catch (err) { next(err) }
}

// ── POST /api/assessments/ayush/vikriti ──────────────────────
exports.vikritiAssessment = async (req, res, next) => {
  try {
    const patient = await Patient.findOne({ user: req.user._id })
    if (!patient) return res.status(400).json({ success: false, message: 'Patient profile not found' })

    const assessment = await Assessment.create({
      patient: patient._id,
      type   : 'ayush',
      'ayush.vikriti': req.body,
      status : 'completed',
    })
    res.status(201).json({ success: true, data: assessment })
  } catch (err) { next(err) }
}
