import { FileText, Search } from 'lucide-react'

export default function Documents() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <FileText size={28} color="var(--ad-indigo)" /> Medical Documents
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '24px' }}>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr><th>Doc ID</th><th>Patient</th><th>Type</th><th>Upload Date</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>#DOC-551</td><td className="admin-fw-600">Patient A</td><td>Lab Report</td><td>Today</td>
                <td><span className="admin-badge-status status-active">Processed</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
