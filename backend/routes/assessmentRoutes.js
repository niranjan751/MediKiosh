'use strict'

const express = require('express')
const router  = express.Router()
const {
  getAssessments, getAssessment, createAssessment, updateAssessment,
  appendTranscript, prakritiAssessment, vikritiAssessment,
} = require('../controllers/assessmentController')
const { protect, authorise } = require('../middleware/authMiddleware')

router.use(protect)

// AYUSH routes (before /:id to avoid collision)
router.post('/ayush/prakriti', prakritiAssessment)
router.post('/ayush/vikriti',  vikritiAssessment)

router.get   ('/',               getAssessments)
router.post  ('/',               createAssessment)
router.get   ('/:id',            getAssessment)
router.put   ('/:id',            updateAssessment)
router.post  ('/:id/transcript', appendTranscript)

module.exports = router
