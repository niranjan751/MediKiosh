import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Mic, MicOff, Send, AlertTriangle } from 'lucide-react'
import aiService from '../../services/aiService'
import assessmentService from '../../services/assessmentService'
import { useAuth } from '../../context/AuthContext'

const LANG_MAP = { en: 'English', ta: 'Tamil', hi: 'Hindi', te: 'Telugu', kn: 'Kannada', ml: 'Malayalam' }

export default function AIInterview() {
  const navigate           = useNavigate()
  const { user }           = useAuth()
  const bottomRef          = useRef(null)
  const [messages,         setMessages]         = useState([])
  const [sessionId,        setSessionId]        = useState(null)
  const [assessmentId,     setAssessmentId]     = useState(null)
  const [currentQuestion,  setCurrentQuestion]  = useState(null)
  const [inputText,        setInputText]        = useState('')
  const [isLoading,        setIsLoading]        = useState(true)
  const [isSubmitting,     setIsSubmitting]     = useState(false)
  const [isCompleted,      setIsCompleted]      = useState(false)
  const [redFlags,         setRedFlags]         = useState([])
  const [language,         setLanguage]         = useState('en')

  // Initialise interview session on mount
  useEffect(() => {
    const init = async () => {
      try {
        setIsLoading(true)

        // 1. Create backend assessment record
        const assessment = await assessmentService.createAssessment({
          language,
          type: 'clinical',
          consentGiven: true,
        })
        setAssessmentId(assessment._id)

        // 2. Start AI interview session
        const startRes = await aiService.startInterview({ language })
        const sid = startRes.session_id
        setSessionId(sid)

        // 3. Get first question
        const qRes = await aiService.getInterviewQuestion(sid)
        if (qRes.question) {
          setCurrentQuestion({ key: qRes.question_key, text: qRes.question, options: qRes.options || [] })
          addMessage('ai', qRes.question)
        }
      } catch (err) {
        addMessage('ai', 'Welcome! I am the MediKiosk AI assistant. Can you tell me what symptoms you are experiencing today?')
        console.error('Interview init error:', err)
      } finally {
        setIsLoading(false)
      }
    }
    init()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const addMessage = (role, text) => {
    setMessages(prev => [...prev, { role, text, ts: new Date() }])
  }

  const handleSend = async (answer = inputText.trim()) => {
    if (!answer || isSubmitting || isCompleted) return
    setInputText('')
    addMessage('user', answer)
    setIsSubmitting(true)

    try {
      let nextQuestion = null
      let completed    = false
      let flags        = []

      if (sessionId) {
        const res = await aiService.submitAnswer({
          session_id:  sessionId,
          question_id: currentQuestion?.key,
          answer,
        })
        completed     = res.completed
        flags         = res.red_flags_detected || []
        nextQuestion  = res.completed ? null : { key: res.next_question_key, text: res.next_question, options: res.options || [] }

        // Persist message to assessment transcript
        if (assessmentId) {
          await assessmentService.appendTranscript(assessmentId, { role: 'patient', message: answer })
          if (res.next_question) {
            await assessmentService.appendTranscript(assessmentId, { role: 'ai', message: res.next_question })
          }
        }

        if (flags.length > 0) setRedFlags(flags)
      }

      if (completed) {
        setIsCompleted(true)
        if (assessmentId) {
          await assessmentService.updateAssessment(assessmentId, { status: 'completed', consentGiven: true })
        }
        addMessage('ai', '✅ Thank you! Your clinical history has been recorded. Please continue to upload any medical documents.')
      } else if (nextQuestion?.text) {
        setCurrentQuestion(nextQuestion)
        addMessage('ai', nextQuestion.text)
      }
    } catch (err) {
      console.error('Submit answer error:', err)
      addMessage('ai', 'I had trouble processing that. Could you please repeat?')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleOptionClick = (option) => {
    const text = typeof option === 'string' ? option : option.label || option.value || option.text
    handleSend(text)
  }

  return (
    <main style={{ height: '100vh', backgroundColor: '#f8fafc', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <header style={{ padding: '16px 32px', backgroundColor: 'white', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexShrink: 0 }}>
        <button onClick={() => navigate('/patient/consent')} style={{ border: 'none', background: 'transparent', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#64748b' }}>
          <ArrowLeft size={16} /> Back
        </button>
        <div style={{ textAlign: 'center' }}>
          <h1 style={{ fontSize: '18px', margin: 0, color: '#1e293b' }}>AI Clinical Interview</h1>
          <p style={{ margin: 0, fontSize: '12px', color: '#64748b' }}>Language: {LANG_MAP[language]} {sessionId && `• Session: ${sessionId.slice(0,8)}…`}</p>
        </div>
        <button
          onClick={() => navigate('/patient/documents')}
          disabled={!isCompleted && messages.length < 3}
          style={{ padding: '8px 16px', background: isCompleted ? '#00897b' : '#1565c0', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', opacity: (!isCompleted && messages.length < 3) ? 0.5 : 1 }}
        >
          {isCompleted ? 'Continue →' : 'Finish Interview'}
        </button>
      </header>

      {/* Red flag alert */}
      {redFlags.length > 0 && (
        <div style={{ backgroundColor: '#fef2f2', border: '1px solid #fecaca', padding: '12px 32px', display: 'flex', alignItems: 'center', gap: '10px', color: '#991b1b', flexShrink: 0 }}>
          <AlertTriangle size={18} />
          <strong>Alert:</strong> Potential clinical red flags detected. Please proceed to the medical staff area.
        </div>
      )}

      {/* Chat messages */}
      <div style={{ flex: 1, padding: '24px 32px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px', maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        {isLoading && (
          <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
            <div style={{ padding: '16px 20px', borderRadius: '16px', backgroundColor: 'white', color: '#64748b', border: '1px solid #e2e8f0' }}>
              Starting interview session…
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx}>
            <div style={{ display: 'flex', justifyContent: msg.role === 'ai' ? 'flex-start' : 'flex-end' }}>
              <div style={{
                maxWidth: '70%', padding: '14px 18px', borderRadius: '16px',
                backgroundColor: msg.role === 'ai' ? 'white' : '#1565c0',
                color: msg.role === 'ai' ? '#1e293b' : 'white',
                boxShadow: '0 2px 4px rgba(0,0,0,0.06)',
                borderBottomLeftRadius: msg.role === 'ai' ? '4px' : '16px',
                borderBottomRightRadius: msg.role === 'user' ? '4px' : '16px',
                fontSize: '15px', lineHeight: '1.6',
                border: msg.role === 'ai' ? '1px solid #e2e8f0' : 'none',
              }}>
                {msg.text}
              </div>
            </div>
            {/* Quick-select options after AI message */}
            {msg.role === 'ai' && idx === messages.length - 1 && currentQuestion?.options?.length > 0 && !isCompleted && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '10px', paddingLeft: '8px' }}>
                {currentQuestion.options.map((opt, oi) => {
                  const label = typeof opt === 'string' ? opt : opt.label || opt.value || JSON.stringify(opt)
                  return (
                    <button
                      key={oi}
                      onClick={() => handleOptionClick(opt)}
                      disabled={isSubmitting}
                      style={{ padding: '8px 14px', backgroundColor: '#f0f7ff', color: '#1565c0', border: '1px solid #bfdbfe', borderRadius: '20px', cursor: 'pointer', fontSize: '13px', fontWeight: '500' }}
                    >
                      {label}
                    </button>
                  )
                })}
              </div>
            )}
          </div>
        ))}

        {isSubmitting && (
          <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
            <div style={{ padding: '14px 18px', borderRadius: '16px', backgroundColor: 'white', color: '#94a3b8', border: '1px solid #e2e8f0', fontSize: '15px' }}>
              Thinking…
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      {!isCompleted && (
        <div style={{ padding: '20px 32px', backgroundColor: 'white', borderTop: '1px solid #e2e8f0', flexShrink: 0, maxWidth: '800px', margin: '0 auto', width: '100%', boxSizing: 'border-box' }}>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-end' }}>
            <textarea
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend() } }}
              placeholder="Type your response or use options above…"
              rows={2}
              style={{ flex: 1, padding: '12px 16px', borderRadius: '12px', border: '1px solid #e2e8f0', resize: 'none', fontSize: '15px', fontFamily: 'inherit', outline: 'none' }}
            />
            <button
              onClick={() => handleSend()}
              disabled={!inputText.trim() || isSubmitting}
              style={{ padding: '14px 20px', backgroundColor: '#1565c0', color: 'white', border: 'none', borderRadius: '12px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '600', opacity: (!inputText.trim() || isSubmitting) ? 0.5 : 1 }}
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      )}

      {isCompleted && (
        <div style={{ padding: '20px 32px', backgroundColor: '#f0fdf4', borderTop: '1px solid #bbf7d0', textAlign: 'center', flexShrink: 0 }}>
          <p style={{ margin: '0 0 12px 0', color: '#166534', fontWeight: '500' }}>Interview complete! Your clinical history has been recorded.</p>
          <button
            onClick={() => navigate('/patient/documents')}
            style={{ padding: '12px 28px', backgroundColor: '#00897b', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', fontSize: '15px' }}
          >
            Continue to Documents →
          </button>
        </div>
      )}
    </main>
  )
}
