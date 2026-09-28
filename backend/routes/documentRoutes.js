'use strict'

const express = require('express')
const router  = express.Router()
const {
  uploadDocument, getDocuments, getDocument, getOCRResult, deleteDocument,
} = require('../controllers/documentController')
const { protect } = require('../middleware/authMiddleware')
const upload = require('../middleware/uploadMiddleware')

router.use(protect)

router.post  ('/',        upload.single('file'), uploadDocument)
router.get   ('/',        getDocuments)
router.get   ('/:id',     getDocument)
router.get   ('/:id/ocr', getOCRResult)
router.delete('/:id',     deleteDocument)

module.exports = router
