import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Save } from 'lucide-react'

export default function Vikriti() {
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
          <h1 style={{ color: 'var(--doc-emerald)' }}>Vikriti Assessment</h1>
          <p>Assess current imbalances.</p>
        </div>

        <div className="pd-card" style={{ maxWidth: '800px', margin: '0 auto' }}>
          <form style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px' }}>Current Digestion (Agni)</label>
              <select style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                <option>Variable / Irregular (Vishamagni)</option>
                <option>Sharp / Intense (Tikshnagni)</option>
                <option>Slow / Sluggish (Mandagni)</option>
                <option>Balanced (Samagni)</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px' }}>Recent Sleep Patterns</label>
              <select style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                <option>Interrupted, light sleep</option>
                <option>Moderate, but wake up easily</option>
                <option>Deep, heavy sleep</option>
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
