import { useNavigate } from 'react-router-dom'
import { ArrowLeft, ArrowRight, Activity, Calendar, FileText } from 'lucide-react'

export default function MedicalTimeline() {
  const navigate = useNavigate()

  return (
    <main style={{ minHeight: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '20px 32px', backgroundColor: 'white', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <button onClick={() => navigate('/patient/documents')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b' }}>
          <ArrowLeft size={16} /> Back
        </button>
        <h1 style={{ fontSize: '20px', margin: 0, color: '#1e293b' }}>Medical Timeline</h1>
        <button onClick={() => navigate('/patient/summary')} style={{ padding: '8px 16px', background: '#1565c0', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}>
          Generate Final Summary
        </button>
      </header>

      <div style={{ flex: 1, padding: '40px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        <h2 style={{ fontSize: '24px', margin: '0 0 32px 0', color: '#1e293b' }}>Your Health Journey</h2>
        
        <div style={{ position: 'relative', borderLeft: '2px solid #e2e8f0', paddingLeft: '32px', marginLeft: '16px' }}>
          
          <div style={{ position: 'relative', marginBottom: '40px' }}>
            <div style={{ position: 'absolute', left: '-49px', top: '0', width: '32px', height: '32px', borderRadius: '50%', backgroundColor: '#e0f2fe', border: '4px solid white', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Activity size={16} color="#0284c7" />
            </div>
            <h3 style={{ margin: '0 0 8px 0', fontSize: '18px', color: '#1e293b' }}>Today's AI Assessment</h3>
            <span style={{ display: 'inline-block', padding: '4px 12px', backgroundColor: '#f1f5f9', color: '#475569', borderRadius: '999px', fontSize: '12px', fontWeight: '600', marginBottom: '12px' }}>Sept 28, 2026</span>
            <p style={{ margin: 0, color: '#475569', backgroundColor: 'white', padding: '16px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>Reported fever, mild cough, and fatigue. Vitals pending.</p>
          </div>

          <div style={{ position: 'relative', marginBottom: '40px' }}>
            <div style={{ position: 'absolute', left: '-49px', top: '0', width: '32px', height: '32px', borderRadius: '50%', backgroundColor: '#fef3c7', border: '4px solid white', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <FileText size={16} color="#b45309" />
            </div>
            <h3 style={{ margin: '0 0 8px 0', fontSize: '18px', color: '#1e293b' }}>Blood Test Report Added</h3>
            <span style={{ display: 'inline-block', padding: '4px 12px', backgroundColor: '#f1f5f9', color: '#475569', borderRadius: '999px', fontSize: '12px', fontWeight: '600', marginBottom: '12px' }}>Sept 28, 2026</span>
            <p style={{ margin: 0, color: '#475569', backgroundColor: 'white', padding: '16px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>Extracted via OCR: Low hemoglobin detected.</p>
          </div>
          
        </div>
      </div>
    </main>
  )
}
