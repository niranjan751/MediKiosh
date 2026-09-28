import { Leaf } from 'lucide-react'

export default function AyushCard({ system, status }) {
  return (
    <div style={{ padding: '24px', borderRadius: '12px', border: '1px solid #e2e8f0', backgroundColor: '#ecfccb', display: 'flex', alignItems: 'center', gap: '16px' }}>
      <div style={{ width: '48px', height: '48px', borderRadius: '50%', backgroundColor: '#d9f99d', color: '#65a30d', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Leaf size={24} />
      </div>
      <div>
        <h4 style={{ margin: '0 0 4px 0', fontSize: '16px', color: '#166534' }}>{system}</h4>
        <p style={{ margin: 0, fontSize: '14px', color: '#15803d' }}>Status: {status}</p>
      </div>
    </div>
  )
}
