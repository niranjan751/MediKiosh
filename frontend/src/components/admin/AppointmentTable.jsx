export default function AppointmentTable({ appointments = [] }) {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ borderBottom: '1px solid #e2e8f0', textAlign: 'left' }}>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Date</th>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Patient</th>
          <th style={{ padding: '12px', color: '#64748b', fontWeight: '600' }}>Status</th>
        </tr>
      </thead>
      <tbody>
        {appointments.map((apt, i) => (
          <tr key={i} style={{ borderBottom: '1px solid #f1f5f9' }}>
            <td style={{ padding: '12px' }}>{apt.date}</td>
            <td style={{ padding: '12px', fontWeight: '500' }}>{apt.patient}</td>
            <td style={{ padding: '12px' }}>{apt.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
