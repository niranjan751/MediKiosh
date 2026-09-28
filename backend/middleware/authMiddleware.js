'use strict'

const jwt  = require('jsonwebtoken')
const User = require('../models/User')

/**
 * Protect route – verifies Bearer JWT.
 * Attaches req.user (without password) on success.
 */
const protect = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ success: false, message: 'Not authorised – no token' })
    }

    const token   = authHeader.split(' ')[1]
    const decoded = jwt.verify(token, process.env.JWT_SECRET)

    const user = await User.findById(decoded.id).select('-password')
    if (!user || !user.isActive) {
      return res.status(401).json({ success: false, message: 'Not authorised – user not found' })
    }

    req.user = user
    next()
  } catch (err) {
    return res.status(401).json({ success: false, message: 'Not authorised – invalid token' })
  }
}

/**
 * Restrict route to specific roles.
 * Usage: router.get('/', protect, authorise('admin', 'doctor'), handler)
 */
const authorise = (...roles) => (req, res, next) => {
  if (!roles.includes(req.user.role)) {
    return res.status(403).json({
      success: false,
      message: `Role '${req.user.role}' is not allowed to access this route`,
    })
  }
  next()
}

module.exports = { protect, authorise }
