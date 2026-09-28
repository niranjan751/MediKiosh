import { useNavigate } from 'react-router-dom'
import { ArrowLeft, ArrowRight, ShieldCheck } from 'lucide-react'

export default function Consent() {
  const navigate = useNavigate()

  return (
    <main style={{ minHeight: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{ maxWidth: '600px', width: '100%', backgroundColor: 'white', borderRadius: '16px', padding: '40px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
        <button onClick={() => navigate('/patient/language')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b', marginBottom: '24px' }}>
          <ArrowLeft size={16} /> Back
        </button>
        
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <ShieldCheck size={48} color="#00897b" style={{ marginBottom: '16px' }} />
          <h1 style={{ fontSize: '28px', color: '#1e293b', margin: '0 0 8px 0', fontFamily: 'Outfit, sans-serif' }}>Data Consent</h1>
          <p style={{ color: '#64748b', margin: 0 }}>Please review how we handle your medical data.</p>
        </div>

        <div style={{ backgroundColor: '#f8fafc', padding: '24px', borderRadius: '12px', marginBottom: '32px', border: '1px solid #e2e8f0', color: '#334155', fontSize: '15px', lineHeight: '1.6' }}>
          <p>By proceeding, you agree to allow MediKiosk to:</p>
          <ul style={{ margin: '12px 0 0 20px', padding: 0 }}>
            <li style={{ marginBottom: '8px' }}>Collect and process your symptoms and medical history via AI.</li>
            <li style={{ marginBottom: '8px' }}>Analyze uploaded documents (prescriptions, lab reports) to extract relevant health data.</li>
            <li style={{ marginBottom: '8px' }}>Share the generated clinical summary with your assigned doctors.</li>
          </ul>
          <p style={{ marginTop: '16px' }}>Your data is encrypted and stored securely in compliance with health data privacy regulations.</p>
        </div>

        <button 
          onClick={() => navigate('/patient/interview')}
          style={{ width: '100%', padding: '16px', background: '#00897b', color: 'white', border: 'none', borderRadius: '12px', fontSize: '18px', fontWeight: 'bold', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', cursor: 'pointer' }}
        >
          I Accept &amp; Continue <ArrowRight size={20} />
        </button>
      </div>
    </main>
  )
}
