import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Search, Filter, Users, ChevronRight } from 'lucide-react'

export default function PatientList() {
  const navigate = useNavigate()

  const PATIENTS = [
    { id: 1, name: 'Patient A', age: 45, gender: 'M', lastVisit: '2026-09-28', status: 'Review Needed' },
    { id: 2, name: 'Patient B', age: 32, gender: 'F', lastVisit: '2026-09-27', status: 'Review Needed' },
    { id: 3, name: 'Patient C', age: 58, gender: 'M', lastVisit: '2026-09-20', status: 'Clear' },
    { id: 4, name: 'Patient D', age: 29, gender: 'F', lastVisit: '2026-09-15', status: 'Clear' },
  ]

  return (
    <main className="doc-layout">
      <header className="doc-navbar">
        <div className="doc-nav-left">
          <button onClick={() => navigate('/dashboard/doctor')} style={{ background: 'transparent', border: 'none', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: 'var(--doc-text-mut)', fontSize: '15px', fontWeight: '500' }}>
            <ArrowLeft size={18} /> Back to Dashboard
          </button>
        </div>
      </header>
      
      <div className="doc-main">
        <div className="doc-welcome">
          <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Users size={32} color="var(--doc-blue)" /> Patient Directory
          </h1>
        </div>

        <div className="doc-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
            <div className="doc-search" style={{ width: '300px' }}>
              <Search size={18} color="var(--doc-text-mut)" />
              <input type="text" placeholder="Search by name or ID..." style={{ width: '100%' }} />
            </div>
            <button className="doc-btn-outline-sm" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Filter size={16} /> Filter
            </button>
          </div>

          <table className="doc-table">
            <thead>
              <tr>
                <th>Patient ID</th>
                <th>Name</th>
                <th>Age / Gender</th>
                <th>Last Visit</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {PATIENTS.map(p => (
                <tr key={p.id} style={{ cursor: 'pointer' }} onClick={() => navigate(`/doctor/patient/${p.id}`)}>
                  <td style={{ color: 'var(--doc-text-mut)' }}>#MK-{1000 + p.id}</td>
                  <td className="doc-fw-600">{p.name}</td>
                  <td>{p.age} yrs / {p.gender}</td>
                  <td>{p.lastVisit}</td>
                  <td>
                    <span className={`badge ${p.status === 'Clear' ? 'badge-completed' : 'badge-pending'}`}>
                      {p.status}
                    </span>
                  </td>
                  <td>
                    <ChevronRight size={20} color="var(--doc-text-mut)" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  )
}
