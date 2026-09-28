import { Users, Search, Filter } from 'lucide-react'

export default function Patients() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Users size={28} color="var(--ad-blue)" /> Patient Management
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
          <div className="admin-search" style={{ width: '300px' }}>
            <Search size={18} color="var(--ad-text-mut)" />
            <input type="text" placeholder="Search patients..." />
          </div>
          <button className="admin-action-btn">
            <Filter size={16} /> Filter
          </button>
        </div>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr><th>ID</th><th>Name</th><th>Phone</th><th>Status</th><th>Action</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>#MK-1001</td><td className="admin-fw-600">Patient A</td><td>+91 9876543210</td>
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
