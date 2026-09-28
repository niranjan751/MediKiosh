import { useNavigate } from 'react-router-dom'
import { ArrowLeft, ArrowRight, CheckCircle2, Globe2, Heart } from 'lucide-react'
import { useState } from 'react'

const LANGUAGES = [
  { id: 'en', name: 'English', native: 'English' },
  { id: 'hi', name: 'Hindi', native: 'हिन्दी' },
  { id: 'ta', name: 'Tamil', native: 'தமிழ்' },
  { id: 'te', name: 'Telugu', native: 'తెలుగు' },
  { id: 'mr', name: 'Marathi', native: 'मराठी' },
  { id: 'bn', name: 'Bengali', native: 'বাংলা' },
]

export default function LanguageSelection() {
  const navigate = useNavigate()
  const [selected, setSelected] = useState('en')

  return (
    <main style={{ minHeight: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{ maxWidth: '600px', width: '100%', backgroundColor: 'white', borderRadius: '16px', padding: '40px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
        <button onClick={() => navigate('/dashboard/patient')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b', marginBottom: '24px' }}>
          <ArrowLeft size={16} /> Back to Dashboard
        </button>
        
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <Globe2 size={48} color="#1565c0" style={{ marginBottom: '16px' }} />
          <h1 style={{ fontSize: '28px', color: '#1e293b', margin: '0 0 8px 0', fontFamily: 'Outfit, sans-serif' }}>Select Your Language</h1>
          <p style={{ color: '#64748b', margin: 0 }}>Choose the language for your health assessment.</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '32px' }}>
          {LANGUAGES.map(lang => (
            <button
              key={lang.id}
              onClick={() => setSelected(lang.id)}
              style={{
                display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '16px 20px',
                border: selected === lang.id ? '2px solid #1565c0' : '1px solid #e2e8f0',
                borderRadius: '12px', background: selected === lang.id ? '#f0f7ff' : 'white',
                cursor: 'pointer', transition: 'all 0.2s',
                color: selected === lang.id ? '#1565c0' : '#1e293b'
              }}
            >
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                <strong style={{ fontSize: '18px' }}>{lang.native}</strong>
                <span style={{ fontSize: '14px', opacity: 0.8 }}>{lang.name}</span>
              </div>
              {selected === lang.id && <CheckCircle2 size={24} />}
            </button>
          ))}
        </div>

        <button 
          onClick={() => navigate('/patient/consent')}
          style={{ width: '100%', padding: '16px', background: '#1565c0', color: 'white', border: 'none', borderRadius: '12px', fontSize: '18px', fontWeight: 'bold', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', cursor: 'pointer' }}
        >
          Continue <ArrowRight size={20} />
        </button>
      </div>
    </main>
  )
}
