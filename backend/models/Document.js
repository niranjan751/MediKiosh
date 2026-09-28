'use strict'

const mongoose = require('mongoose')

const documentSchema = new mongoose.Schema(
  {
    patient      : { type: mongoose.Schema.Types.ObjectId, ref: 'Patient', required: true },
    assessment   : { type: mongoose.Schema.Types.ObjectId, ref: 'Assessment' },
    originalName : { type: String, required: true },
    fileName     : { type: String, required: true },   // stored filename on disk
    filePath     : { type: String, required: true },   // relative path under /uploads
    mimeType     : { type: String, required: true },   // image/jpeg, image/png, application/pdf
    fileSize     : { type: Number },                   // bytes
    ocrStatus    : {
      type   : String,
      enum   : ['pending', 'processing', 'done', 'failed'],
      default: 'pending',
    },
    ocrResult    : {
      rawText   : String,
      diagnosis : [String],
      medications: [String],
      labValues : [Object],
      dates     : [String],
      summary   : String,
    },
    processedAt  : { type: Date },
  },
  { timestamps: true },
)

module.exports = mongoose.model('Document', documentSchema)
