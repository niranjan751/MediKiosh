import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Mic, StopCircle, Check, MessageSquare } from 'lucide-react'
import { useState } from 'react'

export default function AIInterview() {
  const navigate = useNavigate()
  const [isRecording, setIsRecording] = useState(false)
  const [messages, setMessages] = useState([
    { role: 'ai', text: 'Hello Naveen. I am the MediKiosk AI assistant. Can you tell me what symptoms you are experiencing today?' }
  ])

  return (
    <main style={{ height: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '20px 32px', backgroundColor: 'white', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <button onClick={() => navigate('/patient/consent')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b' }}>
          <ArrowLeft size={16} /> Back
        </button>
        <h1 style={{ fontSize: '20px', margin: 0, color: '#1e293b' }}>AI Clinical Interview</h1>
        <button onClick={() => navigate('/patient/documents')} style={{ padding: '8px 16px', background: '#1565c0', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}>
          Finish Interview
        </button>
      </header>

      <div style={{ flex: 1, padding: '32px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ display: 'flex', justifyContent: msg.role === 'ai' ? 'flex-start' : 'flex-end' }}>
            <div style={{
              maxWidth: '70%', padding: '16px 20px', borderRadius: '16px',
              backgroundColor: msg.role === 'ai' ? 'white' : '#1565c0',
              color: msg.role === 'ai' ? '#1e293b' : 'white',
              boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
              borderBottomLeftRadius: msg.role === 'ai' ? '4px' : '16px',
              borderBottomRightRadius: msg.role === 'user' ? '4px' : '16px',
              fontSize: '16px', lineHeight: '1.5'
            }}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      <div style={{ padding: '32px', backgroundColor: 'white', borderTop: '1px solid #e2e8f0', display: 'flex', justifyContent: 'center' }}>
        <button 
          onClick={() => setIsRecording(!isRecording)}
          style={{
            width: '80px', height: '80px', borderRadius: '50%', border: 'none',
            backgroundColor: isRecording ? '#ef4444' : '#1565c0',
            color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center',
            cursor: 'pointer', boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            transition: 'all 0.2s', transform: isRecording ? 'scale(1.05)' : 'scale(1)'
          }}
        >
          {isRecording ? <StopCircle size={36} /> : <Mic size={36} />}
        </button>
      </div>
    </main>
  )
}
