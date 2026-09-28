import { useNavigate } from 'react-router-dom'
import { ArrowLeft, ArrowRight, FileSearch, CheckCircle2 } from 'lucide-react'

export default function OCRResults() {
  const navigate = useNavigate()

  return (
    <main style={{ minHeight: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '20px 32px', backgroundColor: 'white', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <button onClick={() => navigate('/patient/documents')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b' }}>
          <ArrowLeft size={16} /> Back
        </button>
        <h1 style={{ fontSize: '20px', margin: 0, color: '#1e293b' }}>OCR Results</h1>
        <button onClick={() => navigate('/patient/timeline')} style={{ padding: '8px 16px', background: '#00897b', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}>
          Approve &amp; Continue
        </button>
      </header>

      <div style={{ flex: 1, padding: '40px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
          <CheckCircle2 size={32} color="#10b981" />
          <div>
            <h2 style={{ margin: 0, fontSize: '20px', color: '#1e293b' }}>Extraction Complete</h2>
            <p style={{ margin: '4px 0 0 0', color: '#64748b' }}>AI successfully extracted data from "Blood Test Report.pdf"</p>
          </div>
        </div>

        <div style={{ backgroundColor: 'white', borderRadius: '12px', border: '1px solid #e2e8f0', overflow: 'hidden', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
          <div style={{ padding: '16px 24px', backgroundColor: '#f1f5f9', borderBottom: '1px solid #e2e8f0', fontWeight: '600', color: '#334155' }}>
            Extracted Key-Value Pairs
          </div>
          <div style={{ padding: '24px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '150px 1fr', gap: '16px', marginBottom: '16px', borderBottom: '1px dashed #e2e8f0', paddingBottom: '16px' }}>
              <div style={{ color: '#64748b', fontWeight: '500' }}>Patient Name</div>
              <div style={{ color: '#1e293b', fontWeight: '600' }}>Naveen</div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '150px 1fr', gap: '16px', marginBottom: '16px', borderBottom: '1px dashed #e2e8f0', paddingBottom: '16px' }}>
              <div style={{ color: '#64748b', fontWeight: '500' }}>Hemoglobin</div>
              <div style={{ color: '#ef4444', fontWeight: '600' }}>11.2 g/dL (Low)</div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '150px 1fr', gap: '16px' }}>
              <div style={{ color: '#64748b', fontWeight: '500' }}>Test Date</div>
              <div style={{ color: '#1e293b', fontWeight: '600' }}>Sept 28, 2026</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
