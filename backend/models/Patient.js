'use strict'

const mongoose = require('mongoose')

const patientSchema = new mongoose.Schema(
  {
    user        : { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    dateOfBirth : { type: Date },
    gender      : { type: String, enum: ['male', 'female', 'other'] },
    bloodGroup  : { type: String },
    phone       : { type: String, trim: true },
    address     : { type: String, trim: true },
    emergencyContact: {
      name    : String,
      phone   : String,
      relation: String,
    },
    allergies    : [String],
    chronicConditions: [String],
    preferredLanguage: {
      type   : String,
      enum   : ['en', 'ta', 'hi', 'te', 'kn', 'ml'],
      default: 'en',
    },
  },
  { timestamps: true },
)

module.exports = mongoose.model('Patient', patientSchema)
