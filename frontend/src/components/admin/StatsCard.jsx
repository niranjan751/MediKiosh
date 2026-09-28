export default function StatsCard({ label, value, icon: Icon, color = '#3b82f6' }) {
  return (
    <div style={{ backgroundColor: 'white', padding: '24px', borderRadius: '12px', border: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center', boxShadow: '0 1px 2px rgba(0,0,0,0.05)' }}>
      <div>
        <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#64748b', fontWeight: '500' }}>{label}</h3>
        <div style={{ fontSize: '28px', fontWeight: '700', color: '#0f172a' }}>{value}</div>
      </div>
      {Icon && (
        <div style={{ width: '48px', height: '48px', borderRadius: '8px', backgroundColor: `${color}15`, color: color, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Icon size={24} />
        </div>
      )}
    </div>
  )
}
