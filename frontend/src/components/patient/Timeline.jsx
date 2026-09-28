export default function Timeline({ events = [] }) {
  return (
    <div style={{ borderLeft: '2px solid #e2e8f0', marginLeft: '12px', paddingLeft: '24px' }}>
      {events.map((evt, i) => (
        <div key={i} style={{ position: 'relative', marginBottom: '24px' }}>
          <div style={{ position: 'absolute', left: '-33px', top: '4px', width: '16px', height: '16px', borderRadius: '50%', backgroundColor: '#3b82f6', border: '4px solid white' }}></div>
          <div style={{ color: '#64748b', fontSize: '12px', marginBottom: '4px' }}>{evt.date}</div>
          <div style={{ fontWeight: '500', color: '#0f172a' }}>{evt.title}</div>
          <div style={{ color: '#334155', fontSize: '14px' }}>{evt.description}</div>
        </div>
      ))}
    </div>
  )
}
