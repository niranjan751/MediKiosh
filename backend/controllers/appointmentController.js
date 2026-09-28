'use strict'

const Appointment = require('../models/Appointment')
const Patient     = require('../models/Patient')

// ── GET /api/appointments ─────────────────────────────────────
exports.getAppointments = async (req, res, next) => {
  try {
    let query = {}

    if (req.user.role === 'patient') {
      const patient = await Patient.findOne({ user: req.user._id })
      if (patient) query.patient = patient._id
    } else if (req.user.role === 'doctor') {
      // filter by doctor's profile if needed
    }

    const appointments = await Appointment.find(query)
      .populate({ path: 'patient', populate: { path: 'user', select: 'name email' } })
      .populate({ path: 'doctor',  populate: { path: 'user', select: 'name email' } })
      .sort({ date: -1 })

    res.json({ success: true, count: appointments.length, data: appointments })
  } catch (err) { next(err) }
}

// ── GET /api/appointments/:id ─────────────────────────────────
exports.getAppointment = async (req, res, next) => {
  try {
    const appointment = await Appointment.findById(req.params.id)
      .populate({ path: 'patient', populate: { path: 'user', select: 'name email' } })
      .populate({ path: 'doctor',  populate: { path: 'user', select: 'name email' } })
    if (!appointment) return res.status(404).json({ success: false, message: 'Appointment not found' })
    res.json({ success: true, data: appointment })
  } catch (err) { next(err) }
}

// ── POST /api/appointments ────────────────────────────────────
exports.createAppointment = async (req, res, next) => {
  try {
    const { doctor, date, timeSlot, reason } = req.body
    const patient = await Patient.findOne({ user: req.user._id })
    if (!patient) return res.status(400).json({ success: false, message: 'Patient profile not found' })

    const appointment = await Appointment.create({ patient: patient._id, doctor, date, timeSlot, reason })
    res.status(201).json({ success: true, data: appointment })
  } catch (err) { next(err) }
}

// ── PUT /api/appointments/:id ─────────────────────────────────
exports.updateAppointment = async (req, res, next) => {
  try {
    const appointment = await Appointment.findByIdAndUpdate(req.params.id, req.body, {
      new: true, runValidators: true,
    })
    if (!appointment) return res.status(404).json({ success: false, message: 'Appointment not found' })
    res.json({ success: true, data: appointment })
  } catch (err) { next(err) }
}

// ── DELETE /api/appointments/:id ──────────────────────────────
exports.cancelAppointment = async (req, res, next) => {
  try {
    const appointment = await Appointment.findByIdAndUpdate(
      req.params.id,
      { status: 'cancelled' },
      { new: true },
    )
    if (!appointment) return res.status(404).json({ success: false, message: 'Appointment not found' })
    res.json({ success: true, data: appointment })
  } catch (err) { next(err) }
}
