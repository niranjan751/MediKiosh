export default function AssessmentCard({ date, status }) {
  return (
    <div style={{ padding: '16px', border: '1px solid #e2e8f0', borderRadius: '8px', backgroundColor: '#f8fafc', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <div style={{ fontWeight: '500', color: '#0f172a' }}>AI Assessment</div>
        <div style={{ color: '#64748b', fontSize: '14px' }}>{date}</div>
      </div>
      <div style={{ padding: '4px 8px', borderRadius: '4px', backgroundColor: status === 'Completed' ? '#dcfce7' : '#fef3c7', color: status === 'Completed' ? '#166534' : '#b45309', fontSize: '12px', fontWeight: 'bold' }}>
        {status}
      </div>
    </div>
  )
}
