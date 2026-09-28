'use strict'

const express = require('express')
const router  = express.Router()
const {
  getAppointments, getAppointment, createAppointment, updateAppointment, cancelAppointment,
} = require('../controllers/appointmentController')
const { protect } = require('../middleware/authMiddleware')

router.use(protect)

router.get   ('/',    getAppointments)
router.post  ('/',    createAppointment)
router.get   ('/:id', getAppointment)
router.put   ('/:id', updateAppointment)
router.delete('/:id', cancelAppointment)

module.exports = router
