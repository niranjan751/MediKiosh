import { PieChart } from 'lucide-react'

export default function Analytics() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <PieChart size={28} color="var(--ad-blue)" /> Platform Analytics
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '40px', textAlign: 'center' }}>
        <PieChart size={64} color="var(--ad-text-mut)" style={{ marginBottom: '16px' }} />
        <h2>Analytics Dashboard</h2>
        <p style={{ color: 'var(--ad-text-mut)' }}>System metrics, usage charts, and performance graphs will be displayed here.</p>
      </div>
    </>
  )
}
