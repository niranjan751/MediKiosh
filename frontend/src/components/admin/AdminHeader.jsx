import { Search, Bell } from 'lucide-react'

export default function AdminHeader({ title = "Admin Portal" }) {
  return (
    <header className="admin-header" style={{ padding: '16px 32px', display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #e2e8f0', backgroundColor: 'white' }}>
      <h2 style={{ margin: 0, fontSize: '20px', color: '#0f172a' }}>{title}</h2>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', background: '#f1f5f9', padding: '8px 16px', borderRadius: '99px' }}>
          <Search size={16} color="#64748b" />
          <input type="text" placeholder="Search..." style={{ border: 'none', background: 'transparent', marginLeft: '8px', outline: 'none' }} />
        </div>
        <button style={{ background: 'transparent', border: 'none', cursor: 'pointer' }}><Bell size={20} color="#64748b" /></button>
        <div style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: '#3b82f6', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>A</div>
      </div>
    </header>
  )
}
