import { useNavigate } from 'react-router-dom'
import { ArrowLeft, ArrowRight, FileText, UploadCloud, Plus } from 'lucide-react'

export default function Documents() {
  const navigate = useNavigate()

  return (
    <main style={{ minHeight: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '20px 32px', backgroundColor: 'white', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <button onClick={() => navigate('/patient/interview')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b' }}>
          <ArrowLeft size={16} /> Back
        </button>
        <h1 style={{ fontSize: '20px', margin: 0, color: '#1e293b' }}>Medical Documents</h1>
        <button onClick={() => navigate('/patient/timeline')} style={{ padding: '8px 16px', background: '#00897b', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}>
          Continue to Timeline <ArrowRight size={16} style={{ display: 'inline', verticalAlign: 'text-bottom' }}/>
        </button>
      </header>

      <div style={{ flex: 1, padding: '40px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        <div style={{ backgroundColor: 'white', padding: '40px', borderRadius: '16px', border: '2px dashed #cbd5e1', textAlign: 'center', marginBottom: '32px', cursor: 'pointer' }}>
          <UploadCloud size={48} color="#1565c0" style={{ marginBottom: '16px' }} />
          <h2 style={{ fontSize: '20px', color: '#1e293b', margin: '0 0 8px 0' }}>Upload Prescriptions or Reports</h2>
          <p style={{ color: '#64748b', margin: '0 0 24px 0' }}>Tap here to take a photo or upload a file.</p>
          <button style={{ padding: '12px 24px', backgroundColor: '#f0f7ff', color: '#1565c0', border: '1px solid #1565c0', borderRadius: '8px', fontWeight: '600', cursor: 'pointer' }}>
            <Plus size={16} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '8px' }}/> Select File
          </button>
        </div>

        <h3 style={{ fontSize: '18px', color: '#1e293b', marginBottom: '16px' }}>Uploaded Documents</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Example document item */}
          <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <div style={{ width: '48px', height: '48px', backgroundColor: '#e0f2fe', color: '#0284c7', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <FileText size={24} />
              </div>
              <div>
                <h4 style={{ margin: '0 0 4px 0', fontSize: '16px', color: '#1e293b' }}>Blood Test Report.pdf</h4>
                <p style={{ margin: 0, fontSize: '13px', color: '#64748b' }}>Uploaded today • Pending AI extraction</p>
              </div>
            </div>
            <button onClick={() => navigate('/patient/ocr')} style={{ padding: '8px 16px', backgroundColor: 'transparent', color: '#1565c0', border: '1px solid #1565c0', borderRadius: '6px', fontWeight: '600', cursor: 'pointer' }}>
              Process OCR
            </button>
          </div>
        </div>
      </div>
    </main>
  )
}
