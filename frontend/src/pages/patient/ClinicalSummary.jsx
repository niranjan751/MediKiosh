import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Stethoscope, Printer, FileText } from 'lucide-react'

export default function ClinicalSummary() {
  const navigate = useNavigate()

  return (
    <main style={{ minHeight: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '20px 32px', backgroundColor: 'white', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <button onClick={() => navigate('/patient/timeline')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b' }}>
          <ArrowLeft size={16} /> Back
        </button>
        <h1 style={{ fontSize: '20px', margin: 0, color: '#1e293b' }}>AI Clinical Summary</h1>
        <button onClick={() => navigate('/dashboard/patient')} style={{ padding: '8px 16px', background: '#1565c0', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}>
          Back to Dashboard
        </button>
      </header>

      <div style={{ flex: 1, padding: '40px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px' }}>
          <div>
            <h2 style={{ fontSize: '24px', margin: '0 0 8px 0', color: '#1e293b' }}>Consultation Summary</h2>
            <p style={{ margin: 0, color: '#64748b' }}>Generated on Sept 28, 2026 • Ready for Doctor Review</p>
          </div>
          <button style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 16px', border: '1px solid #cbd5e1', backgroundColor: 'white', borderRadius: '8px', color: '#475569', cursor: 'pointer', fontWeight: '500' }}>
            <Printer size={16} /> Print
          </button>
        </div>

        <div style={{ backgroundColor: 'white', padding: '32px', borderRadius: '16px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
          <div style={{ marginBottom: '24px', paddingBottom: '24px', borderBottom: '1px solid #e2e8f0' }}>
            <h3 style={{ fontSize: '16px', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Chief Complaint</h3>
            <p style={{ margin: 0, color: '#1e293b', fontSize: '18px', fontWeight: '500' }}>Patient reports mild fever and continuous fatigue for the past 3 days.</p>
          </div>

          <div style={{ marginBottom: '24px', paddingBottom: '24px', borderBottom: '1px solid #e2e8f0' }}>
            <h3 style={{ fontSize: '16px', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>History of Present Illness</h3>
            <ul style={{ margin: 0, paddingLeft: '20px', color: '#334155', lineHeight: '1.6' }}>
              <li>Onset: 3 days ago</li>
              <li>Severity: Mild to moderate</li>
              <li>Associated symptoms: Dry cough, body ache</li>
              <li>Alleviating factors: Paracetamol provides temporary relief</li>
            </ul>
          </div>

          <div>
            <h3 style={{ fontSize: '16px', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Document Findings</h3>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '16px', backgroundColor: '#fef2f2', borderRadius: '8px', border: '1px solid #fecaca', color: '#991b1b' }}>
              <FileText size={20} />
              <span><strong>Blood Test Report:</strong> Low hemoglobin detected (11.2 g/dL). Requires doctor's attention.</span>
            </div>
          </div>
        </div>

        <div style={{ marginTop: '24px', padding: '16px', backgroundColor: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '12px', color: '#166534' }}>
          <Stethoscope size={24} />
          <span>This summary has been sent to the doctor's queue. Please proceed to the waiting area.</span>
        </div>
      </div>
    </main>
  )
}
