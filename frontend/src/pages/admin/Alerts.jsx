import { AlertTriangle } from 'lucide-react'

export default function Alerts() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <AlertTriangle size={28} color="var(--ad-rose)" /> System Alerts
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '24px' }}>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr><th>Alert ID</th><th>Severity</th><th>Message</th><th>Timestamp</th><th>Action</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>#ALT-901</td><td><span style={{ color: '#e11d48', fontWeight: 'bold' }}>CRITICAL</span></td><td>Doctor verification required</td><td>10 mins ago</td>
                <td><button className="admin-btn-sm">Resolve</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
