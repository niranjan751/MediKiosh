'use strict'

const express = require('express')
const router  = express.Router()
const {
  getPatients, getPatient, getMyProfile, createPatient, updatePatient, deletePatient,
} = require('../controllers/patientController')
const { protect, authorise } = require('../middleware/authMiddleware')

router.use(protect)

router.get   ('/me',  getMyProfile)
router.get   ('/',    authorise('admin', 'doctor'), getPatients)
router.post  ('/',    createPatient)
router.get   ('/:id', getPatient)
router.put   ('/:id', updatePatient)
router.delete('/:id', authorise('admin'), deletePatient)

module.exports = router
