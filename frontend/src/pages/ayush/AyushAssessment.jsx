import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Leaf, ChevronRight } from 'lucide-react'

export default function AyushAssessment() {
  const navigate = useNavigate()

  return (
    <main className="pd-layout">
      <header className="pd-navbar">
        <button className="pd-btn-text" onClick={() => navigate('/dashboard/patient')}>
          <ArrowLeft size={18} /> Back to Dashboard
        </button>
      </header>

      <div className="pd-main">
        <div className="pd-welcome">
          <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--doc-emerald)' }}>
            <Leaf size={32} /> AYUSH Assessment
          </h1>
          <p>Complete your traditional medicine evaluation.</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '16px', maxWidth: '600px', margin: '0 auto' }}>
          
          <div className="pd-card" onClick={() => navigate('/ayush/prakriti')} style={{ cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '18px' }}>Prakriti Analysis</h3>
              <p style={{ margin: 0, color: 'var(--doc-text-mut)' }}>Determine your mind-body constitution (Vata, Pitta, Kapha).</p>
            </div>
            <ChevronRight size={24} color="var(--doc-text-mut)" />
          </div>

          <div className="pd-card" onClick={() => navigate('/ayush/vikriti')} style={{ cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '18px' }}>Vikriti Analysis</h3>
              <p style={{ margin: 0, color: 'var(--doc-text-mut)' }}>Determine your current doshic imbalance.</p>
            </div>
            <ChevronRight size={24} color="var(--doc-text-mut)" />
          </div>

        </div>
      </div>
    </main>
  )
}
