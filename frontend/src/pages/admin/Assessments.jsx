import { Activity, Search } from 'lucide-react'

export default function Assessments() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Activity size={28} color="var(--ad-amber)" /> AI Assessments
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '24px' }}>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr><th>Assessment ID</th><th>Patient</th><th>Date</th><th>AI Score</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>#AS-992</td><td className="admin-fw-600">Patient B</td><td>Today</td><td>8.5/10</td>
                <td><span className="admin-badge-status status-pending">Pending Review</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
