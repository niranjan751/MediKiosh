export default function AyushPractitionerTable({ practitioners = [] }) {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ borderBottom: '1px solid #e2e8f0', textAlign: 'left' }}>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Name</th>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>System</th>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Verified</th>
        </tr>
      </thead>
      <tbody>
        {practitioners.map((p, i) => (
          <tr key={i} style={{ borderBottom: '1px solid #f1f5f9' }}>
            <td style={{ padding: '12px', fontWeight: '600' }}>{p.name}</td>
            <td style={{ padding: '12px' }}>{p.system}</td>
            <td style={{ padding: '12px' }}>{p.verified ? 'Yes' : 'No'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
