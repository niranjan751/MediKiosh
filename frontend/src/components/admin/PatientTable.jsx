export default function PatientTable({ patients = [] }) {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ borderBottom: '1px solid #e2e8f0', textAlign: 'left' }}>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Patient Name</th>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Contact</th>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Status</th>
        </tr>
      </thead>
      <tbody>
        {patients.map((p, i) => (
          <tr key={i} style={{ borderBottom: '1px solid #f1f5f9' }}>
            <td style={{ padding: '12px', fontWeight: '600' }}>{p.name}</td>
            <td style={{ padding: '12px' }}>{p.contact}</td>
            <td style={{ padding: '12px' }}>{p.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
