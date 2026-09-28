export default function ClinicalSummaryCard({ chiefComplaint, history }) {
  return (
    <div style={{ padding: '24px', backgroundColor: 'white', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
      <h3 style={{ margin: '0 0 12px 0', fontSize: '16px', color: '#0f172a' }}>Chief Complaint</h3>
      <p style={{ margin: '0 0 20px 0', fontSize: '14px', color: '#334155' }}>{chiefComplaint}</p>
      <h3 style={{ margin: '0 0 12px 0', fontSize: '16px', color: '#0f172a' }}>History of Present Illness</h3>
      <p style={{ margin: 0, fontSize: '14px', color: '#334155', whiteSpace: 'pre-wrap' }}>{history}</p>
    </div>
  )
}
