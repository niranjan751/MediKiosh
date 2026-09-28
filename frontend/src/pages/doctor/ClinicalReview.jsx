import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, CheckCircle, FileText, Save, Stethoscope } from 'lucide-react'

export default function ClinicalReview() {
  const navigate = useNavigate()
  const { id } = useParams()

  return (
    <main className="doc-layout">
      <header className="doc-navbar">
        <div className="doc-nav-left">
          <button onClick={() => navigate(`/doctor/patient/${id || 1}`)} style={{ background: 'transparent', border: 'none', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: 'var(--doc-text-mut)', fontSize: '15px', fontWeight: '500' }}>
            <ArrowLeft size={18} /> Back to Patient
          </button>
        </div>
        <div className="doc-nav-right">
          <button className="doc-btn-sm" onClick={() => navigate('/dashboard/doctor')} style={{ backgroundColor: 'var(--doc-teal)', color: 'white', borderColor: 'var(--doc-teal)' }}>
            <CheckCircle size={16} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '6px' }} />
            Finalize & Complete
          </button>
        </div>
      </header>

      <div className="doc-main">
        <div className="doc-welcome" style={{ marginBottom: '24px' }}>
          <h1 style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Stethoscope size={32} color="var(--doc-blue)" /> Clinical Review
          </h1>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          
          {/* AI Summary View */}
          <div className="doc-panel" style={{ padding: '32px' }}>
            <h2 style={{ fontSize: '20px', margin: '0 0 24px 0', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <FileText size={24} color="var(--doc-purple)" />
              AI Clinical Summary
            </h2>
            
            <div style={{ marginBottom: '24px' }}>
              <h3 style={{ fontSize: '14px', textTransform: 'uppercase', color: 'var(--doc-text-mut)', letterSpacing: '0.5px', marginBottom: '8px' }}>Chief Complaint</h3>
              <p style={{ margin: 0, fontSize: '16px', lineHeight: '1.6' }}>Patient reports mild fever and continuous fatigue for the past 3 days.</p>
            </div>

            <div style={{ marginBottom: '24px' }}>
              <h3 style={{ fontSize: '14px', textTransform: 'uppercase', color: 'var(--doc-text-mut)', letterSpacing: '0.5px', marginBottom: '8px' }}>History of Present Illness</h3>
              <ul style={{ margin: 0, paddingLeft: '20px', lineHeight: '1.6' }}>
                <li>Onset: 3 days ago</li>
                <li>Severity: Mild to moderate</li>
                <li>Associated symptoms: Dry cough, body ache</li>
              </ul>
            </div>

            <div>
              <h3 style={{ fontSize: '14px', textTransform: 'uppercase', color: 'var(--doc-text-mut)', letterSpacing: '0.5px', marginBottom: '8px' }}>AI Extracted OCR Data</h3>
              <div style={{ padding: '16px', backgroundColor: 'var(--doc-rose-light)', border: '1px solid #fecdd3', borderRadius: '8px', color: '#9f1239' }}>
                <strong>Blood Test Report:</strong> Low hemoglobin detected (11.2 g/dL).
              </div>
            </div>
          </div>

          {/* Doctor Input Form */}
          <div className="doc-panel" style={{ padding: '32px' }}>
            <h2 style={{ fontSize: '20px', margin: '0 0 24px 0', color: 'var(--doc-blue)' }}>Doctor's Notes & Prescription</h2>
            
            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: 'var(--doc-text)' }}>Final Diagnosis</label>
              <input type="text" placeholder="Enter diagnosis..." style={{ width: '100%', padding: '12px 16px', border: '1px solid var(--doc-border)', borderRadius: '8px', fontSize: '15px' }} />
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: 'var(--doc-text)' }}>Prescription & Recommendations</label>
              <textarea placeholder="Write prescription here..." rows={6} style={{ width: '100%', padding: '12px 16px', border: '1px solid var(--doc-border)', borderRadius: '8px', fontSize: '15px', fontFamily: 'inherit', resize: 'vertical' }}></textarea>
            </div>

            <button className="doc-btn-sm" style={{ width: '100%', padding: '14px', fontSize: '15px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
              <Save size={18} /> Save Notes
            </button>
          </div>

        </div>
      </div>
    </main>
  )
}
