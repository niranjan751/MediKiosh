import { FileCheck, Search } from 'lucide-react'

export default function AIReports() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <FileCheck size={28} color="var(--ad-green)" /> AI Reports
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '24px' }}>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr><th>Report ID</th><th>Generated For</th><th>Timestamp</th><th>Confidence</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>#REP-882</td><td className="admin-fw-600">Patient B Assessment</td><td>Today 11:45 AM</td><td>94%</td>
                <td><span className="admin-badge-status status-pending">Awaiting Review</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
