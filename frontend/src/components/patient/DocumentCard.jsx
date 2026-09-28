import { FileText } from 'lucide-react'

export default function DocumentCard({ filename, date }) {
  return (
    <div style={{ padding: '16px', border: '1px solid #e2e8f0', borderRadius: '8px', backgroundColor: 'white', display: 'flex', alignItems: 'center', gap: '12px' }}>
      <div style={{ width: '40px', height: '40px', borderRadius: '8px', backgroundColor: '#eff6ff', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#3b82f6' }}>
        <FileText size={20} />
      </div>
      <div>
        <div style={{ fontWeight: '500', color: '#0f172a', fontSize: '14px' }}>{filename}</div>
        <div style={{ color: '#64748b', fontSize: '12px' }}>Uploaded {date}</div>
      </div>
    </div>
  )
}
