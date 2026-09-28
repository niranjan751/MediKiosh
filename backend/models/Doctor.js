'use strict'

const mongoose = require('mongoose')

const doctorSchema = new mongoose.Schema(
  {
    user          : { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    specialization: { type: String, required: true, trim: true },
    qualification : { type: String, trim: true },
    registrationNo: { type: String, trim: true },
    phone         : { type: String, trim: true },
    department    : { type: String, trim: true },
    experience    : { type: Number, default: 0 },  // years
    isAvailable   : { type: Boolean, default: true },
  },
  { timestamps: true },
)

module.exports = mongoose.model('Doctor', doctorSchema)
