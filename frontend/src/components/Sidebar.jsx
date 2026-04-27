import { useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import {
  LayoutDashboard, Users, MessageSquare, CheckSquare,
  Brain, Settings, Menu, X, Sparkles,
} from 'lucide-react'

const NAV = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/agents', icon: Users, label: 'Équipe IA' },
  { to: '/chat', icon: MessageSquare, label: 'Chat' },
  { to: '/tasks', icon: CheckSquare, label: 'Tâches' },
  { to: '/memory', icon: Brain, label: 'Mémoire' },
  { to: '/settings', icon: Settings, label: 'Paramètres' },
]

export default function Sidebar() {
  const [open, setOpen] = useState(false)
  const navigate = useNavigate()

  const navContent = (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="flex items-center gap-3 px-5 py-5 border-b border-slate-800">
        <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center flex-shrink-0">
          <Sparkles size={16} className="text-white" />
        </div>
        <div className="min-w-0">
          <p className="text-white font-semibold text-sm leading-tight truncate">AI Platform</p>
          <p className="text-slate-500 text-xs truncate">Entrepreneur</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {NAV.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            onClick={() => setOpen(false)}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-150 ${
                isActive
                  ? 'bg-indigo-600 text-white font-medium shadow-sm'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`
            }
          >
            <Icon size={17} className="flex-shrink-0" />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* New Chat button */}
      <div className="p-3 border-t border-slate-800">
        <button
          onClick={() => { navigate('/chat'); setOpen(false) }}
          className="w-full flex items-center justify-center gap-2 px-3 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors"
        >
          <MessageSquare size={15} />
          Nouveau chat
        </button>
      </div>
    </div>
  )

  return (
    <>
      {/* Mobile toggle */}
      <button
        className="md:hidden fixed top-4 left-4 z-50 p-2 bg-slate-900 text-white rounded-lg shadow-lg"
        onClick={() => setOpen(!open)}
      >
        {open ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Mobile overlay */}
      {open && (
        <div
          className="md:hidden fixed inset-0 bg-black/60 z-40"
          onClick={() => setOpen(false)}
        />
      )}

      {/* Sidebar — desktop always visible, mobile slide-in */}
      <aside
        className={`
          fixed md:static inset-y-0 left-0 z-40
          w-56 bg-slate-900 flex-shrink-0
          transform transition-transform duration-200
          ${open ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
        `}
      >
        {navContent}
      </aside>
    </>
  )
}
