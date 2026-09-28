'use strict'

const mongoose = require('mongoose')

const appointmentSchema = new mongoose.Schema(
  {
    patient    : { type: mongoose.Schema.Types.ObjectId, ref: 'Patient', required: true },
    doctor     : { type: mongoose.Schema.Types.ObjectId, ref: 'Doctor',  required: true },
    date       : { type: Date, required: true },
    timeSlot   : { type: String, required: true },   // e.g. "10:00 AM"
    status     : {
      type   : String,
      enum   : ['pending', 'confirmed', 'completed', 'cancelled'],
      default: 'pending',
    },
    reason     : { type: String, trim: true },
    notes      : { type: String, trim: true },
    assessment : { type: mongoose.Schema.Types.ObjectId, ref: 'Assessment' },
  },
  { timestamps: true },
)

module.exports = mongoose.model('Appointment', appointmentSchema)
