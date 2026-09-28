import { useEffect, useState } from 'react'
import Navbar from './components/common/Navbar'
import {
  ArrowRight,
  Brain,
  CheckCircle2,
  ChevronRight,
  Clock,
  FileCheck,
  FileSearch,
  FileText,
  FileUp,
  Heart,
  Languages,
  Lock,
  Mic,
  ShieldCheck,
  Siren,
  Sparkles,
  Sprout,
  Stethoscope,
  UserRoundCheck,
  Zap,
} from 'lucide-react'
import './App.css'

const features = [
  {
    icon: Stethoscope,
    title: 'AI Clinical Interview',
    description: 'Adaptive questions collect patient symptoms and medical history conversationally.',
    colorKey: 'blue',
  },
  {
    icon: Languages,
    title: 'Multilingual Support',
    description: 'Assessments are available in English, Tamil, Hindi, Telugu, Kannada and Malayalam.',
    colorKey: 'emerald',
  },
  {
    icon: FileSearch,
    title: 'Medical Document OCR',
    description: 'Upload JPG, PNG or PDF records and extract useful medical information.',
    colorKey: 'amber',
  },
  {
    icon: Brain,
    title: 'Clinical Summary',
    description: 'Turn collected information into a structured summary for doctor review.',
    colorKey: 'purple',
  },
  {
    icon: Siren,
    title: 'Red-Flag Detection',
    description: 'Identify potentially urgent symptoms and alert healthcare staff for support.',
    colorKey: 'rose',
    alert: true,
  },
  {
    icon: Sprout,
    title: 'AYUSH Assessment',
    description: 'Support Prakriti, Vikriti, Agni, Koshtha, Ahara, Vihara and Dashavidha Pariksha.',
    colorKey: 'teal',
  },
]

const workflowSteps = [
  {
    number: '01',
    phase: 'Patient Intake',
    icon: Languages,
    title: 'Choose Language',
    subtitle: 'Healthcare in your preferred language',
    description: 'Select a language and interact through text, voice, and guided controls.',
    label: 'Languages',
    detail: 'English  •  Tamil  •  Hindi  •  Telugu  •  Kannada  •  Malayalam',
    colorKey: 'emerald',
    badge: 'Multilingual & Voice',
    tags: [
      { code: 'en', label: 'English', native: 'English' },
      { code: 'ta', label: 'Tamil', native: 'தமிழ்' },
      { code: 'hi', label: 'Hindi', native: 'हिंदी' },
      { code: 'te', label: 'Telugu', native: 'తెలుగు' },
      { code: 'kn', label: 'Kannada', native: 'ಕನ್ನಡ' },
      { code: 'ml', label: 'Malayalam', native: 'മലയാളം' },
    ],
    highlight: 'Natural Voice-to-Text & Regional Dialects',
  },
  {
    number: '02',
    phase: 'Privacy & Control',
    icon: ShieldCheck,
    title: 'Give Consent',
    subtitle: 'Your information, your control',
    description: 'Review the purpose of the assessment before sharing medical information.',
    label: 'Highlights',
    detail: 'Clear consent  •  Privacy-focused  •  Patient controlled',
    colorKey: 'rose',
    badge: 'HIPAA & ABDM Aligned',
    securityPoints: [
      'Clear, informed patient consent',
      'Privacy-focused & zero data reselling',
      'Patient retains 100% record control',
    ],
    highlight: '256-Bit Encryption • Sovereign Data Ownership',
  },
  {
    number: '03',
    phase: 'Adaptive Triage',
    icon: Stethoscope,
    title: 'AI Clinical Interview',
    subtitle: 'A smarter way to collect clinical history',
    description: 'Adaptive questions organize symptoms and relevant history from each response.',
    label: 'Example',
    detail: 'Chest Pain  →  Onset  →  Location  →  Radiation  →  Related Symptoms',
    colorKey: 'blue',
    badge: 'Dynamic Questioning',
    pathway: ['Chest Pain', 'Onset', 'Location', 'Radiation', 'Related Symptoms'],
    highlight: 'Instant Red-Flag Detection & Urgency Triage',
  },
  {
    number: '04',
    phase: 'Record Ingestion',
    icon: FileText,
    title: 'Upload Medical Documents',
    subtitle: 'Bring your medical records together',
    description: 'Upload existing medical documents for automated processing.',
    label: 'Supported',
    detail: 'JPG  •  PNG  •  PDF',
    colorKey: 'amber',
    badge: 'Multi-Format Ingest',
    formats: [
      { ext: 'PDF', name: 'Discharge Summaries & Lab Reports' },
      { ext: 'JPG', name: 'Prescriptions & Doctor Slips' },
      { ext: 'PNG', name: 'Diagnostic Scans & Vitals' },
    ],
    highlight: 'Camera Snap or Drag & Drop Batch Upload',
  },
  {
    number: '05',
    phase: 'Neural OCR & Extraction',
    icon: FileSearch,
    title: 'AI Processing',
    subtitle: 'Turn documents into structured information',
    description: 'OCR and clinical processing extract details from your records.',
    label: 'Output',
    detail: 'Diagnosis  •  Medication  •  Lab Values  •  Dates  •  Medical Timeline',
    colorKey: 'purple',
    badge: 'Medical NLP Engine',
    entities: [
      { name: 'Diagnosis', code: 'ICD-10' },
      { name: 'Medication', code: 'Dosages & Rx' },
      { name: 'Lab Values', code: 'Outliers & Trends' },
      { name: 'Dates', code: 'Chronology' },
      { name: 'Medical Timeline', code: 'Longitudinal' },
    ],
    highlight: 'Structured Clinical JSON for Instant EHR Ingest',
  },
  {
    number: '06',
    phase: 'Clinical Approval',
    icon: UserRoundCheck,
    title: 'Doctor Review',
    subtitle: 'Organized information for clinical review',
    description: 'Doctors verify or edit the summary before using it in the clinical workflow.',
    label: 'Doctor View',
    detail: 'Clinical Summary  •  Medical Timeline  •  Alerts  •  Editable Information',
    colorKey: 'teal',
    badge: 'Doctor-in-the-Loop',
    reviewItems: [
      { name: 'Clinical Summary', icon: 'FileText' },
      { name: 'Medical Timeline', icon: 'Clock' },
      { name: 'Alerts', icon: 'Siren' },
      { name: 'Editable Information', icon: 'CheckCircle2' },
    ],
    highlight: 'Cuts Physician Note-Taking Time by up to 70%',
  },
]

const footerGroups = [
  { title: 'Quick Links', links: [['Home', '#home'], ['Features', '#features'], ['How It Works', '#how-it-works'], ['About', '#about'], ['Privacy', '#privacy']] },
  { title: 'Platform', links: [['Patient Portal', '#patient-portal'], ['Doctor Portal', '#doctor-portal'], ['Medical Documents', '#documents'], ['AI Clinical Interview', '#interview'], ['Clinical Summary', '#summary'], ['AYUSH Assessment', '#ayush']] },
  { title: 'Resources', links: [['Help Center', '#help'], ['FAQs', '#faqs'], ['Contact Us', '#contact'], ['Privacy Policy', '#privacy'], ['Terms of Service', '#terms']] },
]

function App() {
  const [currentPage, setCurrentPage] = useState(
    window.location.hash.replace('#', '') || 'home',
  )

  useEffect(() => {
    const handleHashChange = () => {
      setCurrentPage(window.location.hash.replace('#', '') || 'home')
    }

    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  const [activeStage, setActiveStage] = useState('all')
  const [selectedLanguage, setSelectedLanguage] = useState('en')

  const showFeatures = currentPage === 'home' || currentPage === 'features'
  const showWorkflow = currentPage === 'how-it-works' || currentPage === 'home'

  const filteredSteps = workflowSteps.filter((_, idx) => {
    if (activeStage === 'patient') return idx < 3
    if (activeStage === 'clinical') return idx >= 3
    return true
  })

  return (
    <div id="top">
      <Navbar />
      <main id="home">
        {currentPage === 'home' && (
          <section className="intro-hero" aria-label="MediKiosk introduction">
            <div className="intro-hero-content">
              <span className="intro-hero-badge">
                <Sparkles size={15} strokeWidth={2} aria-hidden="true" />
                AI-Powered Healthcare Platform
              </span>
              <p>
                MediKiosk helps patients record their clinical history, organize medical documents, and share structured health information with doctors through an AI-assisted, multilingual platform
              </p>
              <div className="intro-hero-actions">
                <a className="intro-hero-button intro-hero-primary" href="#assessment">
                  Start Your Health Assessment <ArrowRight size={17} aria-hidden="true" />
                </a>
                <a className="intro-hero-button intro-hero-secondary" href="#how-it-works">
                  Explore How It Works
                </a>
              </div>
            </div>
          </section>
        )}
        {showFeatures && (
          <section className="features-section" id="features" aria-labelledby="features-title">
            <div className="features-heading">
              <span className="section-kicker">Built for better care</span>
              <h1 id="features-title">Powerful Healthcare Features</h1>
              <p>AI-powered tools for faster and organized clinical assessment.</p>
            </div>
            <div className="features-grid">
              {features.map(({ icon: Icon, title, description, colorKey, alert }) => (
                <article className={`feature-card feature-card-${colorKey}${alert ? ' feature-card-alert' : ''}`} key={title}>
                  <div className="feature-icon" aria-hidden="true"><Icon size={24} strokeWidth={1.9} /></div>
                  <h2>{title}</h2>
                  <p>{description}</p>
                </article>
              ))}
            </div>
          </section>
        )}
        {showWorkflow && (
          <section className="workflow-section" id="how-it-works" aria-labelledby="workflow-title">
            <div className="workflow-bg-glow" aria-hidden="true" />

            <div className="features-heading workflow-heading">
              <h1 id="workflow-title">How MediKiosk Works</h1>
              <p>From patient input to doctor-ready information.</p>

              {/* Stage Filter Switcher */}
              <div className="workflow-stage-tabs" role="tablist" aria-label="Workflow Stages">
                <button
                  type="button"
                  role="tab"
                  aria-selected={activeStage === 'all'}
                  className={`stage-tab-btn ${activeStage === 'all' ? 'is-active' : ''}`}
                  onClick={() => setActiveStage('all')}
                >
                  All 6 Steps
                </button>
                <button
                  type="button"
                  role="tab"
                  aria-selected={activeStage === 'patient'}
                  className={`stage-tab-btn ${activeStage === 'patient' ? 'is-active' : ''}`}
                  onClick={() => setActiveStage('patient')}
                >
                  <span className="stage-num-pill">01–03</span> Patient Journey
                </button>
                <button
                  type="button"
                  role="tab"
                  aria-selected={activeStage === 'clinical'}
                  className={`stage-tab-btn ${activeStage === 'clinical' ? 'is-active' : ''}`}
                  onClick={() => setActiveStage('clinical')}
                >
                  <span className="stage-num-pill">04–06</span> AI & Clinical Engine
                </button>
              </div>

              {/* Connected Step Pipeline Tracker */}
              <div className="workflow-stepper-tracker" aria-hidden="true">
                <div className="stepper-track-line" />
                <div className="stepper-nodes">
                  {workflowSteps.map((s, idx) => {
                    const isVisible =
                      activeStage === 'all' ||
                      (activeStage === 'patient' && idx < 3) ||
                      (activeStage === 'clinical' && idx >= 3)
                    return (
                      <div
                        key={s.number}
                        className={`stepper-node stepper-node-${s.colorKey} ${isVisible ? 'is-active-stage' : 'is-dimmed'}`}
                      >
                        <span className="stepper-node-dot">{s.number}</span>
                        <span className="stepper-node-label">{s.title}</span>
                      </div>
                    )
                  })}
                </div>
              </div>
            </div>

            <div className="workflow-grid">
              {filteredSteps.map(({
                number,
                phase,
                icon: Icon,
                title,
                subtitle,
                description,
                label,
                detail,
                colorKey,
                badge,
                tags,
                securityPoints,
                pathway,
                formats,
                entities,
                reviewItems,
                highlight,
              }) => (
                <article className={`feature-card workflow-step-${colorKey}`} key={number}>
                  <div className="feature-icon" aria-hidden="true">
                    <Icon size={24} strokeWidth={1.9} />
                  </div>
                  <h2>{title}</h2>
                  <p className="workflow-card-subtitle">{subtitle}</p>
                  <p>{description}</p>
                </article>
              ))}
            </div>

            <div className="workflow-cta">
              <div className="workflow-cta-content">
                <span className="section-kicker">Your next step</span>
                <h2>Ready to simplify clinical history?</h2>
                <p>Start your MediKiosk health assessment and experience the complete workflow.</p>
                <div className="workflow-cta-badges">
                  <span className="cta-micro-badge"><CheckCircle2 size={13} /> Zero Waiting Queues</span>
                  <span className="cta-micro-badge"><CheckCircle2 size={13} /> 6 Languages Supported</span>
                  <span className="cta-micro-badge"><CheckCircle2 size={13} /> Doctor-Approved Summary</span>
                </div>
              </div>
              <a className="nav-cta workflow-nav-cta" href="#assessment">
                Get Started <ArrowRight size={17} aria-hidden="true" />
              </a>
            </div>
          </section>
        )}
      </main>
      <footer className="site-footer">
        <div className="footer-main">
          <div className="footer-brand">
            <a className="footer-logo" href="#top">
              <span className="footer-logo-mark" aria-hidden="true"><Heart size={18} fill="currentColor" /></span>
              <strong>MediKiosk</strong>
            </a>
            <p>AI-powered clinical history and medical document digitization for a smarter healthcare experience.</p>
            <span className="footer-tags">AI-Assisted  •  Multilingual  •  Privacy-Focused</span>
          </div>
          {footerGroups.map(({ title, links }) => (
            <div className="footer-group" key={title}>
              <h2>{title}</h2>
              {links.map(([label, href]) => <a href={href} key={label}>{label}</a>)}
            </div>
          ))}
        </div>
        <div className="footer-cta">
          <div>
            <h2>Ready to get started?</h2>
            <p>Start your health assessment with MediKiosk.</p>
          </div>
          <a className="nav-cta" href="#assessment">Start Assessment <ArrowRight size={17} aria-hidden="true" /></a>
        </div>
        <div className="footer-bottom">
          <span>© 2026 MediKiosk. All rights reserved.</span>
          <span>AI-assisted healthcare information platform.</span>
        </div>
      </footer>
    </div>
  )
}

export default App
