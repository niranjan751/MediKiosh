'use strict'

const express = require('express')
const router  = express.Router()
const {
  getDoctors, getDoctor, createDoctor, updateDoctor, deleteDoctor,
} = require('../controllers/doctorController')
const { protect, authorise } = require('../middleware/authMiddleware')

router.use(protect)

router.get   ('/',    getDoctors)
router.post  ('/',    authorise('admin'), createDoctor)
router.get   ('/:id', getDoctor)
router.put   ('/:id', authorise('admin', 'doctor'), updateDoctor)
router.delete('/:id', authorise('admin'), deleteDoctor)

module.exports = router
