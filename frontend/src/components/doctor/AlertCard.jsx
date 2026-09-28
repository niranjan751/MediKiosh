import { AlertTriangle } from 'lucide-react'

export default function AlertCard({ type, message }) {
  const isCritical = type === 'critical'
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '16px', borderRadius: '8px', backgroundColor: isCritical ? '#fff1f2' : '#eff6ff', border: `1px solid ${isCritical ? '#fecdd3' : '#bfdbfe'}`, color: isCritical ? '#9f1239' : '#1e3a8a' }}>
      <AlertTriangle size={20} />
      <span style={{ fontWeight: '500', fontSize: '14px' }}>{message}</span>
    </div>
  )
}
