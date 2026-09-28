import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Calendar as CalendarIcon, Clock, MapPin, X } from 'lucide-react'
import appointmentService from '../../services/appointmentService'

export default function Appointments() {
  const navigate = useNavigate()
  const [appointments, setAppointments] = useState([])
  const [loading,      setLoading]      = useState(true)
  const [error,        setError]        = useState('')

  useEffect(() => {
    appointmentService.getAppointments()
      .then(res => setAppointments(res.data || []))
      .catch(() => setError('Unable to load appointments.'))
      .finally(() => setLoading(false))
  }, [])

  const handleCancel = async (id) => {
    if (!window.confirm('Cancel this appointment?')) return
    try {
      await appointmentService.cancelAppointment(id)
      setAppointments(prev => prev.filter(a => a._id !== id))
    } catch {
      alert('Could not cancel. Please try again.')
    }
  }

  return (
    <main style={{ minHeight: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '20px 32px', backgroundColor: 'white', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <button onClick={() => navigate('/dashboard/patient')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b' }}>
          <ArrowLeft size={16} /> Back to Dashboard
        </button>
        <h1 style={{ fontSize: '20px', margin: 0, color: '#1e293b' }}>My Appointments</h1>
        <div style={{ width: '140px' }} />
      </header>

      <div style={{ flex: 1, padding: '40px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
          <h2 style={{ fontSize: '24px', margin: 0, color: '#1e293b' }}>Upcoming</h2>
          <button
            style={{ padding: '10px 20px', backgroundColor: '#1565c0', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}
            onClick={() => navigate('/dashboard/patient')}
          >
            Book New Appointment
          </button>
        </div>

        {loading && (
          <p style={{ color: '#64748b', textAlign: 'center' }}>Loading appointments…</p>
        )}
        {error && (
          <p style={{ color: '#ef4444', textAlign: 'center' }}>{error}</p>
        )}

        {!loading && appointments.length === 0 && !error && (
          <div style={{ backgroundColor: 'white', padding: '32px', borderRadius: '16px', border: '1px solid #e2e8f0', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', minHeight: '300px' }}>
            <div style={{ backgroundColor: '#f1f5f9', padding: '24px', borderRadius: '50%', marginBottom: '24px' }}>
              <CalendarIcon size={48} color="#64748b" />
            </div>
            <h3 style={{ fontSize: '20px', margin: '0 0 8px 0', color: '#1e293b' }}>No Appointments Scheduled</h3>
            <p style={{ margin: '0 0 24px 0', color: '#64748b', maxWidth: '400px' }}>You do not have any upcoming consultations. Would you like to book one now?</p>
            <button style={{ padding: '12px 24px', backgroundColor: '#e0f2fe', color: '#0284c7', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}>
              Book Appointment
            </button>
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {appointments.map((apt) => (
            <div key={apt._id} style={{ backgroundColor: 'white', padding: '20px 24px', borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <h3 style={{ margin: '0 0 8px 0', color: '#1e293b' }}>
                    Dr. {apt.doctor?.user?.name || 'Assigned Doctor'}
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    <span style={{ color: '#64748b', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <CalendarIcon size={14} /> {apt.date ? new Date(apt.date).toLocaleDateString() : 'TBD'}
                    </span>
                    {apt.timeSlot && (
                      <span style={{ color: '#64748b', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <Clock size={14} /> {apt.timeSlot}
                      </span>
                    )}
                    {apt.reason && (
                      <span style={{ color: '#64748b', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <MapPin size={14} /> {apt.reason}
                      </span>
                    )}
                  </div>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '8px' }}>
                  <span style={{
                    padding: '4px 10px', borderRadius: '999px', fontSize: '12px', fontWeight: '600',
                    backgroundColor: apt.status === 'confirmed' ? '#dcfce7' : apt.status === 'cancelled' ? '#fee2e2' : '#fef9c3',
                    color: apt.status === 'confirmed' ? '#166534' : apt.status === 'cancelled' ? '#991b1b' : '#854d0e',
                  }}>
                    {apt.status || 'pending'}
                  </span>
                  {apt.status !== 'cancelled' && (
                    <button
                      onClick={() => handleCancel(apt._id)}
                      style={{ background: 'transparent', border: '1px solid #e2e8f0', borderRadius: '6px', padding: '4px 10px', cursor: 'pointer', color: '#64748b', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px' }}
                    >
                      <X size={12} /> Cancel
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}
