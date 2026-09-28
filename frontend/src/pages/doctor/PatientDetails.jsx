import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, User, Activity, FileText, Calendar, Edit3 } from 'lucide-react'

export default function PatientDetails() {
  const navigate = useNavigate()
  const { id } = useParams()

  return (
    <main className="doc-layout">
      <header className="doc-navbar">
        <div className="doc-nav-left">
          <button onClick={() => navigate('/dashboard/doctor/patients')} style={{ background: 'transparent', border: 'none', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: 'var(--doc-text-mut)', fontSize: '15px', fontWeight: '500' }}>
            <ArrowLeft size={18} /> Back to Directory
          </button>
        </div>
        <div className="doc-nav-right">
          <button className="doc-btn-sm" onClick={() => navigate(`/doctor/review/${id || 1}`)} style={{ backgroundColor: 'var(--doc-blue)', color: 'white' }}>
            <Edit3 size={16} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '6px' }} />
            Start Clinical Review
          </button>
        </div>
      </header>

      <div className="doc-main">
        <div style={{ display: 'flex', gap: '24px', alignItems: 'flex-start' }}>
          
          {/* Left Profile Sidebar */}
          <div className="doc-panel" style={{ flex: '0 0 320px', padding: '32px 24px', textAlign: 'center' }}>
            <div style={{ width: '80px', height: '80px', borderRadius: '50%', backgroundColor: 'var(--doc-blue-light)', color: 'var(--doc-blue)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px auto' }}>
              <User size={40} />
            </div>
            <h2 style={{ margin: '0 0 8px 0', fontSize: '22px' }}>Patient {id === '2' ? 'B' : 'A'}</h2>
            <p style={{ color: 'var(--doc-text-mut)', margin: '0 0 24px 0' }}>#MK-{1000 + parseInt(id || '1')} • 45 yrs • Male</p>
            
            <div style={{ textAlign: 'left', borderTop: '1px solid var(--doc-border)', paddingTop: '24px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                <Activity size={18} color="var(--doc-text-mut)" />
                <span style={{ color: 'var(--doc-text)' }}>Blood Type: O+</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                <Calendar size={18} color="var(--doc-text-mut)" />
                <span style={{ color: 'var(--doc-text)' }}>Registered: Jan 2026</span>
              </div>
            </div>
          </div>

          {/* Right Content */}
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '24px' }}>
            
            {/* Vitals Summary */}
            <div className="doc-panel" style={{ padding: '24px' }}>
              <h3 style={{ margin: '0 0 16px 0', fontSize: '18px' }}>Recent Vitals</h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
                <div style={{ backgroundColor: 'var(--doc-bg)', padding: '16px', borderRadius: '8px', border: '1px solid var(--doc-border)' }}>
                  <div style={{ fontSize: '13px', color: 'var(--doc-text-mut)', marginBottom: '4px' }}>BP</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: 'var(--doc-text)' }}>120/80</div>
                </div>
                <div style={{ backgroundColor: 'var(--doc-bg)', padding: '16px', borderRadius: '8px', border: '1px solid var(--doc-border)' }}>
                  <div style={{ fontSize: '13px', color: 'var(--doc-text-mut)', marginBottom: '4px' }}>Heart Rate</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: 'var(--doc-text)' }}>72 bpm</div>
                </div>
                <div style={{ backgroundColor: 'var(--doc-bg)', padding: '16px', borderRadius: '8px', border: '1px solid var(--doc-border)' }}>
                  <div style={{ fontSize: '13px', color: 'var(--doc-text-mut)', marginBottom: '4px' }}>Temp</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: 'var(--doc-text)' }}>98.6 °F</div>
                </div>
                <div style={{ backgroundColor: 'var(--doc-bg)', padding: '16px', borderRadius: '8px', border: '1px solid var(--doc-border)' }}>
                  <div style={{ fontSize: '13px', color: 'var(--doc-text-mut)', marginBottom: '4px' }}>SpO2</div>
                  <div style={{ fontSize: '20px', fontWeight: '700', color: 'var(--doc-text)' }}>99%</div>
                </div>
              </div>
            </div>

            {/* Documents */}
            <div className="doc-panel" style={{ padding: '24px' }}>
              <h3 style={{ margin: '0 0 16px 0', fontSize: '18px' }}>Uploaded Documents</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '16px', backgroundColor: 'var(--doc-bg)', border: '1px solid var(--doc-border)', borderRadius: '8px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <FileText size={20} color="var(--doc-blue)" />
                    <span style={{ fontWeight: '500' }}>Blood_Test_Report_Sept_2026.pdf</span>
                  </div>
                  <button className="doc-btn-outline-sm">View</button>
                </div>
              </div>
            </div>
            
          </div>
        </div>
      </div>
    </main>
  )
}
