export default function PatientCard({ name, age, gender }) {
  return (
    <div style={{ padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0', backgroundColor: 'white', display: 'flex', alignItems: 'center', gap: '16px' }}>
      <div style={{ width: '48px', height: '48px', borderRadius: '50%', backgroundColor: '#eff6ff', color: '#3b82f6', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
        {name.charAt(0)}
      </div>
      <div>
        <h4 style={{ margin: '0 0 4px 0', fontSize: '16px' }}>{name}</h4>
        <p style={{ margin: 0, fontSize: '14px', color: '#64748b' }}>{age} yrs • {gender}</p>
      </div>
    </div>
  )
}
