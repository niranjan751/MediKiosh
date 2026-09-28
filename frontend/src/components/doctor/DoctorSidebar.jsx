export default function DoctorSidebar() {
  return (
    <aside style={{ width: '240px', backgroundColor: '#f8fafc', borderRight: '1px solid #e2e8f0', height: '100vh', padding: '24px' }}>
      <h3 style={{ margin: '0 0 24px 0', color: '#64748b', fontSize: '14px', textTransform: 'uppercase' }}>Menu</h3>
      <nav style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <a href="/dashboard/doctor" style={{ color: '#0f172a', textDecoration: 'none', fontWeight: '500' }}>Dashboard</a>
        <a href="/dashboard/doctor/patients" style={{ color: '#0f172a', textDecoration: 'none', fontWeight: '500' }}>Patients</a>
      </nav>
    </aside>
  )
}
