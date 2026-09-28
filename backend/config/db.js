// ============================================================
// MEDIKIOSK – MongoDB / Mongoose Connection
// ============================================================

'use strict'

const mongoose = require('mongoose')

/**
 * Connects to MongoDB using the MONGO_URI environment variable.
 * Exits the process if the initial connection fails so the server
 * doesn't start in a broken state.
 */
async function connectDB () {
  const uri = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/medikiosk'

  try {
    await mongoose.connect(uri)
    console.log(`✅  MongoDB connected → ${mongoose.connection.host}/${mongoose.connection.name}`)
  } catch (err) {
    console.error('❌  MongoDB connection error:', err.message)
    process.exit(1)
  }

  // Log any post-startup disconnections
  mongoose.connection.on('disconnected', () => {
    console.warn('⚠️   MongoDB disconnected')
  })

  mongoose.connection.on('reconnected', () => {
    console.log('✅  MongoDB reconnected')
  })
}

module.exports = connectDB
