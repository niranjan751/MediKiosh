import { Calendar, Search } from 'lucide-react'

export default function Appointments() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Calendar size={28} color="var(--ad-purple)" /> Appointments
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '24px' }}>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr><th>Date/Time</th><th>Patient</th><th>Doctor</th><th>Type</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>Sept 28, 09:30 AM</td><td className="admin-fw-600">Patient A</td><td>Dr. Kumar</td><td>Consultation</td>
                <td><span className="admin-badge-status status-pending">Scheduled</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
