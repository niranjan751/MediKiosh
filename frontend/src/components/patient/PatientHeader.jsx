export default function PatientHeader({ name }) {
  return (
    <header style={{ padding: '16px 32px', borderBottom: '1px solid #e2e8f0', backgroundColor: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <h2 style={{ margin: 0, fontSize: '20px', color: '#0f172a' }}>MediKiosk Patient Portal</h2>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', fontWeight: '500' }}>
        <span>Welcome, {name}</span>
      </div>
    </header>
  )
}
