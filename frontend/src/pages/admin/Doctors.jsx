import { Stethoscope, Search, Plus } from 'lucide-react'

export default function Doctors() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px', margin: 0 }}>
          <Stethoscope size={28} color="var(--ad-teal)" /> Doctor Management
        </h1>
        <button className="admin-action-btn" style={{ backgroundColor: 'var(--ad-teal)', color: 'white' }}>
          <Plus size={18} /> Add Doctor
        </button>
      </div>
      
      <div className="admin-panel" style={{ padding: '24px' }}>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr><th>ID</th><th>Name</th><th>Department</th><th>Status</th><th>Action</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>#DR-205</td><td className="admin-fw-600">Dr. Kumar</td><td>Cardiology</td>
                <td><span className="admin-badge-status status-active">Active</span></td>
                <td><button className="admin-btn-sm">View</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
