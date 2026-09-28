import { FileDigit } from 'lucide-react'

export default function ABDM() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <FileDigit size={28} color="var(--ad-blue)" /> ABDM Compliance
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '24px' }}>
        <p style={{ color: 'var(--ad-text-mut)', marginBottom: '24px' }}>Monitor Ayushman Bharat Digital Mission (ABDM) metrics.</p>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr><th>Metric</th><th>Total Count</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr>
                <td className="admin-fw-600">ABHA IDs Generated</td><td>4,250</td>
                <td><span className="admin-badge-status status-active">Operational</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
