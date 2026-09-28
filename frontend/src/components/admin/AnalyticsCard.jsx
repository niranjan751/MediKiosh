export default function AnalyticsCard({ title, data }) {
  return (
    <div style={{ backgroundColor: 'white', padding: '24px', borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 1px 2px rgba(0,0,0,0.05)' }}>
      <h3 style={{ margin: '0 0 16px 0', fontSize: '16px', color: '#0f172a' }}>{title}</h3>
      <div style={{ height: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f8fafc', borderRadius: '8px', color: '#64748b' }}>
        [Chart Graphic Placeholder: {data?.length || 0} items]
      </div>
    </div>
  )
}
