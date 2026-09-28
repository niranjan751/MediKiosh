import { LayoutDashboard, Users, Settings } from 'lucide-react'

export default function AdminSidebar() {
  return (
    <aside style={{ width: '260px', backgroundColor: '#0f172a', color: 'white', display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <div style={{ padding: '24px', borderBottom: '1px solid #1e293b' }}>
        <h2 style={{ margin: 0, fontSize: '20px' }}>MediKiosk Admin</h2>
      </div>
      <nav style={{ padding: '24px 16px', flex: 1, display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <a href="/dashboard/admin" style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '12px', color: 'white', textDecoration: 'none', borderRadius: '8px', background: '#3b82f6' }}>
          <LayoutDashboard size={18} /> Dashboard
        </a>
        <a href="/admin/patients" style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '12px', color: '#94a3b8', textDecoration: 'none', borderRadius: '8px' }}>
          <Users size={18} /> Patients
        </a>
        <a href="/admin/settings" style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '12px', color: '#94a3b8', textDecoration: 'none', borderRadius: '8px' }}>
          <Settings size={18} /> Settings
        </a>
      </nav>
    </aside>
  )
}
