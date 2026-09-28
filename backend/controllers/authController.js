'use strict'

const jwt     = require('jsonwebtoken')
const User    = require('../models/User')
const Patient = require('../models/Patient')

// ── helpers ──────────────────────────────────────────────────
const signToken = (id) =>
  jwt.sign({ id }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || '7d',
  })

const sendToken = (user, statusCode, res) => {
  const token = signToken(user._id)
  res.status(statusCode).json({ success: true, token, user })
}

// ── POST /api/auth/register ───────────────────────────────────
exports.register = async (req, res, next) => {
  try {
    const { name, email, password, role } = req.body

    if (!name || !email || !password)
      return res.status(400).json({ success: false, message: 'Name, email and password are required' })

    const existing = await User.findOne({ email })
    if (existing)
      return res.status(409).json({ success: false, message: 'Email already registered' })

    const user = await User.create({ name, email, password, role: role || 'patient' })

    // Auto-create Patient profile if role is patient
    if (user.role === 'patient') {
      await Patient.create({ user: user._id })
    }

    sendToken(user, 201, res)
  } catch (err) {
    next(err)
  }
}

// ── POST /api/auth/login ──────────────────────────────────────
exports.login = async (req, res, next) => {
  try {
    const { email, password } = req.body

    if (!email || !password)
      return res.status(400).json({ success: false, message: 'Email and password are required' })

    const user = await User.findOne({ email }).select('+password')
    if (!user || !(await user.matchPassword(password)))
      return res.status(401).json({ success: false, message: 'Invalid email or password' })

    if (!user.isActive)
      return res.status(403).json({ success: false, message: 'Account is deactivated' })

    sendToken(user, 200, res)
  } catch (err) {
    next(err)
  }
}

// ── GET /api/auth/me ──────────────────────────────────────────
exports.getMe = async (req, res, next) => {
  try {
    const user = await User.findById(req.user._id)
    res.json({ success: true, user })
  } catch (err) {
    next(err)
  }
}

// ── POST /api/auth/logout ─────────────────────────────────────
exports.logout = (_req, res) => {
  // JWT is stateless – client must discard the token
  res.json({ success: true, message: 'Logged out successfully' })
}
