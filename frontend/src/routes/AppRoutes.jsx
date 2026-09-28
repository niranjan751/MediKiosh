import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

// Landing
import App from '../App'

// Auth flow
import Login      from '../pages/auth/Login'
import Signup     from '../pages/auth/Signup'
import RoleSelect from '../pages/auth/RoleSelect'

// Dashboards
import PatientDashboard from '../pages/patient/PatientDashboard'
import LanguageSelection from '../pages/patient/LanguageSelection'
import Consent           from '../pages/patient/Consent'
import AIInterview       from '../pages/patient/AIInterview'
import Documents         from '../pages/patient/Documents'
import OCRResults        from '../pages/patient/OCRResults'
import MedicalTimeline   from '../pages/patient/MedicalTimeline'
import ClinicalSummary   from '../pages/patient/ClinicalSummary'
import Appointments      from '../pages/patient/Appointments'

import DoctorDashboard  from '../pages/doctor/DoctorDashboard'
import PatientList      from '../pages/doctor/PatientList'
import PatientDetails   from '../pages/doctor/PatientDetails'
import ClinicalReview   from '../pages/doctor/ClinicalReview'

import AyushAssessment  from '../pages/ayush/AyushAssessment'
import Prakriti         from '../pages/ayush/Prakriti'
import Vikriti          from '../pages/ayush/Vikriti'

import AdminLayout      from '../pages/admin/AdminLayout'
import AdminDashboard   from '../pages/admin/AdminDashboard'
import AdminPatients    from '../pages/admin/Patients'
import AdminDoctors     from '../pages/admin/Doctors'
import AdminAppointments from '../pages/admin/Appointments'
import AdminAssessments from '../pages/admin/Assessments'
import AdminDocuments   from '../pages/admin/Documents'
import AdminAIReports   from '../pages/admin/AIReports'
import AdminAlerts      from '../pages/admin/Alerts'
import AdminAnalytics   from '../pages/admin/Analytics'
import AdminAYUSH       from '../pages/admin/AYUSH'
import AdminABDM        from '../pages/admin/ABDM'
import AdminConsent     from '../pages/admin/Consent'
import AdminSettings    from '../pages/admin/Settings'

/**
 * Auth flow:
 *   /  →  /login | /signup  →  /select-role  →  /dashboard/:role
 */
function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ── Public ── */}
        <Route path="/"      element={<App />}    />
        <Route path="/login" element={<Login />}  />
        <Route path="/signup" element={<Signup />} />

        {/* ── Role selection (post-auth) ── */}
        <Route path="/select-role" element={<RoleSelect />} />

        {/* ── Dashboards ── */}
        <Route path="/dashboard/patient" element={<PatientDashboard />} />
        <Route path="/dashboard/doctor"  element={<DoctorDashboard />}  />
        
        {/* ── Admin Journey (Nested Layout) ── */}
        <Route element={<AdminLayout />}>
          <Route path="/dashboard/admin"   element={<AdminDashboard />} />
          <Route path="/admin/patients"    element={<AdminPatients />} />
          <Route path="/admin/doctors"     element={<AdminDoctors />} />
          <Route path="/admin/appointments" element={<AdminAppointments />} />
          <Route path="/admin/assessments" element={<AdminAssessments />} />
          <Route path="/admin/documents"   element={<AdminDocuments />} />
          <Route path="/admin/reports"     element={<AdminAIReports />} />
          <Route path="/admin/alerts"      element={<AdminAlerts />} />
          <Route path="/admin/analytics"   element={<AdminAnalytics />} />
          <Route path="/admin/ayush"       element={<AdminAYUSH />} />
          <Route path="/admin/abdm"        element={<AdminABDM />} />
          <Route path="/admin/consent"     element={<AdminConsent />} />
          <Route path="/admin/settings"    element={<AdminSettings />} />
        </Route>

        {/* ── Patient Journey ── */}
        <Route path="/patient/language" element={<LanguageSelection />} />
        <Route path="/patient/consent" element={<Consent />} />
        <Route path="/patient/interview" element={<AIInterview />} />
        <Route path="/patient/documents" element={<Documents />} />
        <Route path="/patient/ocr" element={<OCRResults />} />
        <Route path="/patient/timeline" element={<MedicalTimeline />} />
        <Route path="/patient/summary" element={<ClinicalSummary />} />
        <Route path="/appointments" element={<Appointments />} />
        
        {/* ── AYUSH Journey ── */}
        <Route path="/ayush" element={<AyushAssessment />} />
        <Route path="/ayush/prakriti" element={<Prakriti />} />
        <Route path="/ayush/vikriti" element={<Vikriti />} />

        {/* ── Doctor Journey ── */}
        <Route path="/dashboard/doctor/patients" element={<PatientList />} />
        <Route path="/doctor/patient/:id" element={<PatientDetails />} />
        <Route path="/doctor/review/:id" element={<ClinicalReview />} />

        {/* Redirects from dashboard shortcuts */}
        <Route path="/assessment" element={<Navigate to="/patient/language" replace />} />
        <Route path="/documents" element={<Navigate to="/patient/documents" replace />} />
        <Route path="/history" element={<Navigate to="/patient/timeline" replace />} />
        <Route path="/summary" element={<Navigate to="/patient/summary" replace />} />

        {/* ── Catch-all ── */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRoutes
