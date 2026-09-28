export default function AppointmentCard({ date, doctor, department }) {
  return (
    <div style={{ padding: '16px', border: '1px solid #e2e8f0', borderRadius: '8px', backgroundColor: 'white' }}>
      <div style={{ color: '#64748b', fontSize: '14px', marginBottom: '8px' }}>{date}</div>
      <div style={{ fontWeight: '600', color: '#0f172a' }}>{doctor}</div>
      <div style={{ color: '#3b82f6', fontSize: '14px' }}>{department}</div>
    </div>
  )
}
