import { ShieldCheck } from 'lucide-react'

export default function Consent() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <ShieldCheck size={28} color="var(--ad-teal)" /> Data Consent Logs
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '24px' }}>
        <p style={{ color: 'var(--ad-text-mut)', marginBottom: '24px' }}>Audit trail for patient data privacy consent.</p>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr><th>Consent ID</th><th>Patient</th><th>Agreed On</th><th>Version</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>#CON-9921</td><td className="admin-fw-600">Patient A</td><td>Sept 28, 2026</td><td>v1.2</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
