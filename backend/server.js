// ============================================================
// MEDIKIOSK BACKEND SERVER
// ============================================================

'use strict'

const express   = require('express')
const cors      = require('cors')
const dotenv    = require('dotenv')
const path      = require('path')
const fs        = require('fs')

// Load environment variables first
dotenv.config()

// ============================================================
// DATABASE CONNECTION
// ============================================================
const connectDB = require('./config/db')

// ============================================================
// ROUTE IMPORTS
// ============================================================
const authRoutes        = require('./routes/authRoutes')
const patientRoutes     = require('./routes/patientRoutes')
const doctorRoutes      = require('./routes/doctorRoutes')
const appointmentRoutes = require('./routes/appointmentRoutes')
const assessmentRoutes  = require('./routes/assessmentRoutes')
const documentRoutes    = require('./routes/documentRoutes')

// ============================================================
// APP SETUP
// ============================================================
const app  = express()
const PORT = process.env.PORT || 5000

// ============================================================
// ENSURE UPLOAD DIRECTORY EXISTS
// ============================================================
const uploadDir = path.join(__dirname, 'uploads')
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true })
}

// ============================================================
// GLOBAL MIDDLEWARE
// ============================================================
app.use(cors({
  origin: process.env.CLIENT_ORIGIN || 'http://localhost:5174',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}))

app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true, limit: '10mb' }))

// Serve uploaded files statically
app.use('/uploads', express.static(uploadDir))

// ============================================================
// REQUEST LOGGER (dev)
// ============================================================
if (process.env.NODE_ENV !== 'production') {
  app.use((req, _res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl}`)
    next()
  })
}

// ============================================================
// API ROUTES
// ============================================================

// Health check (no auth required)
app.get('/api/health', (_req, res) => {
  res.json({
    service : 'MediKiosk Backend',
    status  : 'healthy',
    version : '1.0.0',
    timestamp: new Date().toISOString(),
  })
})

// Mount route modules
app.use('/api/auth',         authRoutes)
app.use('/api/patients',     patientRoutes)
app.use('/api/doctors',      doctorRoutes)
app.use('/api/appointments', appointmentRoutes)
app.use('/api/assessments',  assessmentRoutes)
app.use('/api/documents',    documentRoutes)

// ============================================================
// 404 HANDLER
// ============================================================
app.use((_req, res) => {
  res.status(404).json({ success: false, message: 'Route not found' })
})

// ============================================================
// GLOBAL ERROR HANDLER
// ============================================================
// eslint-disable-next-line no-unused-vars
app.use((err, _req, res, _next) => {
  console.error('[Error]', err.message)
  const status = err.status || err.statusCode || 500
  res.status(status).json({
    success : false,
    message : err.message || 'Internal Server Error',
    ...(process.env.NODE_ENV !== 'production' && { stack: err.stack }),
  })
})

// ============================================================
// START SERVER
// ============================================================
async function startServer () {
  // Connect to MongoDB (exits process on failure)
  await connectDB()

  app.listen(PORT, () => {
    console.log('============================================================')
    console.log('  MediKiosk Backend Server')
    console.log(`  Running  →  http://localhost:${PORT}`)
    console.log(`  Health   →  http://localhost:${PORT}/api/health`)
    console.log(`  Env      →  ${process.env.NODE_ENV || 'development'}`)
    console.log('============================================================')
  })
}

startServer()
