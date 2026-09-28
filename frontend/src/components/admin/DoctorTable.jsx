export default function DoctorTable({ doctors = [] }) {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ borderBottom: '1px solid #e2e8f0', textAlign: 'left' }}>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Doctor Name</th>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Department</th>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Status</th>
        </tr>
      </thead>
      <tbody>
        {doctors.map((doc, i) => (
          <tr key={i} style={{ borderBottom: '1px solid #f1f5f9' }}>
            <td style={{ padding: '12px', fontWeight: '600' }}>{doc.name}</td>
            <td style={{ padding: '12px' }}>{doc.department}</td>
            <td style={{ padding: '12px' }}>{doc.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
