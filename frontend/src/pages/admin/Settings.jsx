import { Settings as SettingsIcon } from 'lucide-react'

export default function Settings() {
  return (
    <>
      <div className="admin-welcome" style={{ marginBottom: '24px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <SettingsIcon size={28} color="var(--ad-text)" /> Platform Settings
        </h1>
      </div>
      
      <div className="admin-panel" style={{ padding: '40px', maxWidth: '600px' }}>
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px' }}>Hospital Name</label>
          <input type="text" defaultValue="MediKiosk General Hospital" style={{ width: '100%', padding: '12px', border: '1px solid var(--ad-border)', borderRadius: '8px' }} />
        </div>
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px' }}>AI Model Threshold</label>
          <input type="number" defaultValue={0.85} step={0.01} style={{ width: '100%', padding: '12px', border: '1px solid var(--ad-border)', borderRadius: '8px' }} />
        </div>
        <button className="admin-btn-sm" style={{ padding: '12px 24px' }}>Save Changes</button>
      </div>
    </>
  )
}
