import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Calendar as CalendarIcon, Clock, MapPin } from 'lucide-react'

export default function Appointments() {
  const navigate = useNavigate()

  return (
    <main style={{ minHeight: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '20px 32px', backgroundColor: 'white', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <button onClick={() => navigate('/dashboard/patient')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b' }}>
          <ArrowLeft size={16} /> Back to Dashboard
        </button>
        <h1 style={{ fontSize: '20px', margin: 0, color: '#1e293b' }}>My Appointments</h1>
        <div style={{ width: '100px' }}></div> {/* Spacer */}
      </header>

      <div style={{ flex: 1, padding: '40px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
          <h2 style={{ fontSize: '24px', margin: 0, color: '#1e293b' }}>Upcoming</h2>
          <button style={{ padding: '10px 20px', backgroundColor: '#1565c0', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}>
            Book New Appointment
          </button>
        </div>

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
      </div>
    </main>
  )
}
