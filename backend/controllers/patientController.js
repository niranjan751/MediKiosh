'use strict'

const Patient = require('../models/Patient')
const User    = require('../models/User')

// ── GET /api/patients ─────────────────────────────────────────
exports.getPatients = async (req, res, next) => {
  try {
    const patients = await Patient.find().populate('user', 'name email role')
    res.json({ success: true, count: patients.length, data: patients })
  } catch (err) { next(err) }
}

// ── GET /api/patients/:id ─────────────────────────────────────
exports.getPatient = async (req, res, next) => {
  try {
    const patient = await Patient.findById(req.params.id).populate('user', 'name email')
    if (!patient) return res.status(404).json({ success: false, message: 'Patient not found' })
    res.json({ success: true, data: patient })
  } catch (err) { next(err) }
}

// ── GET /api/patients/me ──────────────────────────────────────
exports.getMyProfile = async (req, res, next) => {
  try {
    const patient = await Patient.findOne({ user: req.user._id }).populate('user', 'name email')
    if (!patient) return res.status(404).json({ success: false, message: 'Patient profile not found' })
    res.json({ success: true, data: patient })
  } catch (err) { next(err) }
}

// ── POST /api/patients ────────────────────────────────────────
exports.createPatient = async (req, res, next) => {
  try {
    const existing = await Patient.findOne({ user: req.user._id })
    if (existing) return res.status(409).json({ success: false, message: 'Patient profile already exists' })

    const patient = await Patient.create({ user: req.user._id, ...req.body })
    res.status(201).json({ success: true, data: patient })
  } catch (err) { next(err) }
}

// ── PUT /api/patients/:id ─────────────────────────────────────
exports.updatePatient = async (req, res, next) => {
  try {
    const patient = await Patient.findByIdAndUpdate(req.params.id, req.body, {
      new: true, runValidators: true,
    })
    if (!patient) return res.status(404).json({ success: false, message: 'Patient not found' })
    res.json({ success: true, data: patient })
  } catch (err) { next(err) }
}

// ── DELETE /api/patients/:id ──────────────────────────────────
exports.deletePatient = async (req, res, next) => {
  try {
    const patient = await Patient.findByIdAndDelete(req.params.id)
    if (!patient) return res.status(404).json({ success: false, message: 'Patient not found' })
    // Also deactivate the linked user
    await User.findByIdAndUpdate(patient.user, { isActive: false })
    res.json({ success: true, message: 'Patient deleted' })
  } catch (err) { next(err) }
}
