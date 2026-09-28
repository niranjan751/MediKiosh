import { useState } from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import {
  Activity,
  AlertTriangle,
  Calendar,
  FileText,
  Heart,
  LogOut,
  Settings,
  Users,
  Search,
  Stethoscope,
  PieChart,
  Leaf,
  ShieldCheck,
  FileDigit,
  LayoutDashboard
} from 'lucide-react'
import './AdminDashboard.css'

export default function AdminLayout() {
  const navigate = useNavigate()
  const location = useLocation()

  const NAV_LINKS = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, route: '/dashboard/admin' },
    { id: 'patients', label: 'Patients', icon: Users, route: '/admin/patients' },
    { id: 'doctors', label: 'Doctors', icon: Stethoscope, route: '/admin/doctors' },
    { id: 'appointments', label: 'Appointments', icon: Calendar, route: '/admin/appointments' },
    { id: 'assessments', label: 'Assessments', icon: Activity, route: '/admin/assessments' },
    { id: 'documents', label: 'Documents', icon: FileText, route: '/admin/documents' },
    { id: 'reports', label: 'AI Reports', icon: FileText, route: '/admin/reports' },
    { id: 'alerts', label: 'Alerts', icon: AlertTriangle, route: '/admin/alerts' },
    { id: 'analytics', label: 'Analytics', icon: PieChart, route: '/admin/analytics' },
    { id: 'ayush', label: 'AYUSH', icon: Leaf, route: '/admin/ayush' },
    { id: 'abdm', label: 'ABDM', icon: FileDigit, route: '/admin/abdm' },
    { id: 'consent', label: 'Consent', icon: ShieldCheck, route: '/admin/consent' },
    { id: 'settings', label: 'Settings', icon: Settings, route: '/admin/settings' },
  ]

  const isActive = (route) => {
    if (route === '/dashboard/admin' && location.pathname === '/dashboard/admin') return true
    if (route !== '/dashboard/admin' && location.pathname.startsWith(route)) return true
    return false
  }

  return (
    <div className="admin-layout">
      {/* Sidebar */}
      <aside className="admin-sidebar">
        <div className="admin-brand">
          <div className="admin-brand-icon"><Heart size={20} fill="currentColor" /></div>
          <h2>MediKiosk <span className="admin-badge">Admin</span></h2>
        </div>
        <nav className="admin-nav">
          {NAV_LINKS.map(link => (
            <button 
              key={link.id} 
              className={`admin-nav-link ${isActive(link.route) ? 'active' : ''}`}
              onClick={() => navigate(link.route)}
            >
              <link.icon size={18} />
              <span>{link.label}</span>
            </button>
          ))}
        </nav>
        <div className="admin-sidebar-footer">
          <button className="admin-logout-btn" onClick={() => navigate('/login')}>
            <LogOut size={16} /> Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="admin-main">
        {/* Top Header */}
        <header className="admin-header">
          <div className="admin-search">
            <Search size={18} />
            <input type="text" placeholder="Search users, documents, settings..." />
          </div>
          <div className="admin-profile">
            <div className="admin-avatar">A</div>
            <span>Super Admin</span>
          </div>
        </header>

        {/* Page Content Rendered Here */}
        <div className="admin-content">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
