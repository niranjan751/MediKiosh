import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Save } from 'lucide-react'

export default function Prakriti() {
  const navigate = useNavigate()

  return (
    <main className="pd-layout">
      <header className="pd-navbar">
        <button className="pd-btn-text" onClick={() => navigate('/ayush')}>
          <ArrowLeft size={18} /> Back to AYUSH
        </button>
      </header>

      <div className="pd-main">
        <div className="pd-welcome">
          <h1 style={{ color: 'var(--doc-emerald)' }}>Prakriti Assessment</h1>
        </div>

        <div className="pd-card" style={{ maxWidth: '800px', margin: '0 auto' }}>
          <form style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px' }}>Body Frame</label>
              <select style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                <option>Thin and narrow</option>
                <option>Moderate</option>
                <option>Broad and well-built</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px' }}>Skin Type</label>
              <select style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                <option>Dry and rough</option>
                <option>Warm and sensitive</option>
                <option>Thick and oily</option>
              </select>
            </div>
            
            <button type="button" className="pd-btn-primary" style={{ backgroundColor: 'var(--doc-emerald)', borderColor: 'var(--doc-emerald)', display: 'flex', justifyContent: 'center', gap: '8px' }}>
              <Save size={18} /> Save Assessment
            </button>
          </form>
        </div>
      </div>
    </main>
  )
}
