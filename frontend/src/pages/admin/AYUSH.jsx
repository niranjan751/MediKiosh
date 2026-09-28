import { Leaf, Search } from 'lucide-react'

export default function AYUSH() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Leaf size={28} color="var(--ad-emerald)" /> AYUSH Integration
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '24px' }}>
        <p style={{ color: 'var(--ad-text-mut)', marginBottom: '24px' }}>Manage traditional medicine records and practitioners.</p>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr><th>Reg ID</th><th>Practitioner</th><th>System</th><th>Verified</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>#AYU-102</td><td className="admin-fw-600">Dr. Sharma</td><td>Ayurveda</td>
                <td><span className="admin-badge-status status-active">Yes</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
