'use strict'

const mongoose = require('mongoose')
const bcrypt   = require('bcryptjs')

const userSchema = new mongoose.Schema(
  {
    name    : { type: String, required: true, trim: true },
    email   : { type: String, required: true, unique: true, lowercase: true, trim: true },
    password: { type: String, required: true, minlength: 6, select: false },
    role    : { type: String, enum: ['patient', 'doctor', 'admin'], default: 'patient' },
    isActive: { type: Boolean, default: true },
  },
  { timestamps: true },
)

// Hash password before saving
userSchema.pre('save', async function () {
  if (!this.isModified('password')) return
  this.password = await bcrypt.hash(this.password, 12)
})

// Compare password helper
userSchema.methods.matchPassword = function (enteredPassword) {
  return bcrypt.compare(enteredPassword, this.password)
}

// Never return password in JSON responses
userSchema.set('toJSON', {
  transform (doc, ret) {
    delete ret.password
    return ret
  },
})

module.exports = mongoose.model('User', userSchema)
