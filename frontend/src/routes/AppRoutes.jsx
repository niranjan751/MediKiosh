import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'

// Landing
import App from '../App'

// Auth flow
import Login      from '../pages/auth/Login'
import Signup     from '../pages/auth/Signup'
import RoleSelect from '../pages/auth/RoleSelect'

// Patient pages
import PatientDashboard from '../pages/patient/PatientDashboard'
import LanguageSelection from '../pages/patient/LanguageSelection'
import Consent           from '../pages/patient/Consent'
import AIInterview       from '../pages/patient/AIInterview'
import Documents         from '../pages/patient/Documents'
import OCRResults        from '../pages/patient/OCRResults'
import MedicalTimeline   from '../pages/patient/MedicalTimeline'
import ClinicalSummary   from '../pages/patient/ClinicalSummary'
import Appointments      from '../pages/patient/Appointments'

// Doctor pages
import DoctorDashboard  from '../pages/doctor/DoctorDashboard'
import PatientList      from '../pages/doctor/PatientList'
import PatientDetails   from '../pages/doctor/PatientDetails'
import ClinicalReview   from '../pages/doctor/ClinicalReview'

// AYUSH pages
import AyushAssessment  from '../pages/ayush/AyushAssessment'
import Prakriti         from '../pages/ayush/Prakriti'
import Vikriti          from '../pages/ayush/Vikriti'

// Admin pages
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
 *   /  →  /login | /signup  →  /dashboard/:role
 */
function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ── Public ── */}
        <Route path="/"       element={<App />}    />
        <Route path="/login"  element={<Login />}  />
        <Route path="/signup" element={<Signup />} />

        {/* ── Role selection (post-auth) ── */}
        <Route path="/select-role" element={<ProtectedRoute><RoleSelect /></ProtectedRoute>} />

        {/* ── Patient Dashboard ── */}
        <Route path="/dashboard/patient" element={
          <ProtectedRoute roles={['patient', 'admin']}>
            <PatientDashboard />
          </ProtectedRoute>
        } />

        {/* ── Patient Journey ── */}
        <Route path="/patient/language"  element={<ProtectedRoute roles={['patient']}><LanguageSelection /></ProtectedRoute>} />
        <Route path="/patient/consent"   element={<ProtectedRoute roles={['patient']}><Consent /></ProtectedRoute>} />
        <Route path="/patient/interview" element={<ProtectedRoute roles={['patient']}><AIInterview /></ProtectedRoute>} />
        <Route path="/patient/documents" element={<ProtectedRoute roles={['patient']}><Documents /></ProtectedRoute>} />
        <Route path="/patient/ocr"       element={<ProtectedRoute roles={['patient']}><OCRResults /></ProtectedRoute>} />
        <Route path="/patient/timeline"  element={<ProtectedRoute roles={['patient']}><MedicalTimeline /></ProtectedRoute>} />
        <Route path="/patient/summary"   element={<ProtectedRoute roles={['patient']}><ClinicalSummary /></ProtectedRoute>} />
        <Route path="/appointments"      element={<ProtectedRoute roles={['patient']}><Appointments /></ProtectedRoute>} />

        {/* ── Doctor Dashboard ── */}
        <Route path="/dashboard/doctor" element={
          <ProtectedRoute roles={['doctor', 'admin']}>
            <DoctorDashboard />
          </ProtectedRoute>
        } />
        <Route path="/dashboard/doctor/patients" element={<ProtectedRoute roles={['doctor', 'admin']}><PatientList /></ProtectedRoute>} />
        <Route path="/doctor/patient/:id"        element={<ProtectedRoute roles={['doctor', 'admin']}><PatientDetails /></ProtectedRoute>} />
        <Route path="/doctor/review/:id"         element={<ProtectedRoute roles={['doctor', 'admin']}><ClinicalReview /></ProtectedRoute>} />

        {/* ── AYUSH Journey ── */}
        <Route path="/ayush"          element={<ProtectedRoute roles={['patient']}><AyushAssessment /></ProtectedRoute>} />
        <Route path="/ayush/prakriti" element={<ProtectedRoute roles={['patient']}><Prakriti /></ProtectedRoute>} />
        <Route path="/ayush/vikriti"  element={<ProtectedRoute roles={['patient']}><Vikriti /></ProtectedRoute>} />

        {/* ── Admin Journey (Nested Layout) ── */}
        <Route element={<ProtectedRoute roles={['admin']}><AdminLayout /></ProtectedRoute>}>
          <Route path="/dashboard/admin"    element={<AdminDashboard />} />
          <Route path="/admin/patients"     element={<AdminPatients />} />
          <Route path="/admin/doctors"      element={<AdminDoctors />} />
          <Route path="/admin/appointments" element={<AdminAppointments />} />
          <Route path="/admin/assessments"  element={<AdminAssessments />} />
          <Route path="/admin/documents"    element={<AdminDocuments />} />
          <Route path="/admin/reports"      element={<AdminAIReports />} />
          <Route path="/admin/alerts"       element={<AdminAlerts />} />
          <Route path="/admin/analytics"    element={<AdminAnalytics />} />
          <Route path="/admin/ayush"        element={<AdminAYUSH />} />
          <Route path="/admin/abdm"         element={<AdminABDM />} />
          <Route path="/admin/consent"      element={<AdminConsent />} />
          <Route path="/admin/settings"     element={<AdminSettings />} />
        </Route>

        {/* Shortcut redirects */}
        <Route path="/assessment" element={<Navigate to="/patient/language" replace />} />
        <Route path="/documents"  element={<Navigate to="/patient/documents" replace />} />
        <Route path="/history"    element={<Navigate to="/patient/timeline" replace />} />
        <Route path="/summary"    element={<Navigate to="/patient/summary" replace />} />

        {/* ── Catch-all ── */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRoutes
