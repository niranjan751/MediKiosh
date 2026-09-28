'use strict'

const Doctor = require('../models/Doctor')

// ── GET /api/doctors ──────────────────────────────────────────
exports.getDoctors = async (_req, res, next) => {
  try {
    const doctors = await Doctor.find().populate('user', 'name email')
    res.json({ success: true, count: doctors.length, data: doctors })
  } catch (err) { next(err) }
}

// ── GET /api/doctors/:id ──────────────────────────────────────
exports.getDoctor = async (req, res, next) => {
  try {
    const doctor = await Doctor.findById(req.params.id).populate('user', 'name email')
    if (!doctor) return res.status(404).json({ success: false, message: 'Doctor not found' })
    res.json({ success: true, data: doctor })
  } catch (err) { next(err) }
}

// ── POST /api/doctors ─────────────────────────────────────────
exports.createDoctor = async (req, res, next) => {
  try {
    const doctor = await Doctor.create(req.body)
    res.status(201).json({ success: true, data: doctor })
  } catch (err) { next(err) }
}

// ── PUT /api/doctors/:id ──────────────────────────────────────
exports.updateDoctor = async (req, res, next) => {
  try {
    const doctor = await Doctor.findByIdAndUpdate(req.params.id, req.body, {
      new: true, runValidators: true,
    })
    if (!doctor) return res.status(404).json({ success: false, message: 'Doctor not found' })
    res.json({ success: true, data: doctor })
  } catch (err) { next(err) }
}

// ── DELETE /api/doctors/:id ───────────────────────────────────
exports.deleteDoctor = async (req, res, next) => {
  try {
    const doctor = await Doctor.findByIdAndDelete(req.params.id)
    if (!doctor) return res.status(404).json({ success: false, message: 'Doctor not found' })
    res.json({ success: true, message: 'Doctor deleted' })
  } catch (err) { next(err) }
}
