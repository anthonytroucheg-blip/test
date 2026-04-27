import { useNavigate } from 'react-router-dom'
import {
  Network, TrendingUp, Tent, MapPin, Zap, Target, MessageSquare,
} from 'lucide-react'

const ICONS = { Network, TrendingUp, Tent, MapPin, Zap, Target }

const COLOR_MAP = {
  indigo: {
    bg: 'bg-indigo-50', border: 'border-indigo-100',
    icon: 'bg-indigo-600 text-white', badge: 'bg-indigo-100 text-indigo-700',
    btn: 'bg-indigo-600 hover:bg-indigo-700 text-white',
  },
  emerald: {
    bg: 'bg-emerald-50', border: 'border-emerald-100',
    icon: 'bg-emerald-600 text-white', badge: 'bg-emerald-100 text-emerald-700',
    btn: 'bg-emerald-600 hover:bg-emerald-700 text-white',
  },
  amber: {
    bg: 'bg-amber-50', border: 'border-amber-100',
    icon: 'bg-amber-500 text-white', badge: 'bg-amber-100 text-amber-700',
    btn: 'bg-amber-500 hover:bg-amber-600 text-white',
  },
  blue: {
    bg: 'bg-blue-50', border: 'border-blue-100',
    icon: 'bg-blue-600 text-white', badge: 'bg-blue-100 text-blue-700',
    btn: 'bg-blue-600 hover:bg-blue-700 text-white',
  },
  orange: {
    bg: 'bg-orange-50', border: 'border-orange-100',
    icon: 'bg-orange-500 text-white', badge: 'bg-orange-100 text-orange-700',
    btn: 'bg-orange-500 hover:bg-orange-600 text-white',
  },
  violet: {
    bg: 'bg-violet-50', border: 'border-violet-100',
    icon: 'bg-violet-600 text-white', badge: 'bg-violet-100 text-violet-700',
    btn: 'bg-violet-600 hover:bg-violet-700 text-white',
  },
}

export default function AgentCard({ agent, compact = false }) {
  const navigate = useNavigate()
  const Icon = ICONS[agent.icon] || Network
  const colors = COLOR_MAP[agent.color] || COLOR_MAP.indigo

  const handleChat = async () => {
    const { createConversation } = await import('../services/api')
    const conv = await createConversation({ agent_id: agent.id, title: `Chat avec ${agent.name}` })
    navigate(`/chat/${conv.id}`)
  }

  if (compact) {
    return (
      <div className={`flex items-center gap-3 p-3 rounded-xl border ${colors.border} ${colors.bg}`}>
        <div className={`w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 ${colors.icon}`}>
          <Icon size={16} />
        </div>
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium text-slate-800 truncate">{agent.name}</p>
          <p className="text-xs text-slate-500 truncate">{agent.role}</p>
        </div>
        <button onClick={handleChat} className="p-1.5 rounded-lg hover:bg-white/60 text-slate-500 hover:text-indigo-600 transition-colors">
          <MessageSquare size={15} />
        </button>
      </div>
    )
  }

  return (
    <div className={`rounded-2xl border p-6 flex flex-col gap-4 ${colors.bg} ${colors.border} hover:shadow-md transition-shadow`}>
      <div className="flex items-start gap-4">
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm ${colors.icon}`}>
          <Icon size={22} />
        </div>
        <div className="min-w-0 flex-1">
          <h3 className="font-semibold text-slate-800 text-base">{agent.name}</h3>
          <p className="text-sm text-slate-500">{agent.role}</p>
        </div>
      </div>

      <p className="text-sm text-slate-600 leading-relaxed">{agent.description}</p>

      <div className="flex flex-wrap gap-1.5">
        {agent.expertise.slice(0, 3).map((e) => (
          <span key={e} className={`text-xs px-2.5 py-1 rounded-full font-medium ${colors.badge}`}>
            {e}
          </span>
        ))}
        {agent.expertise.length > 3 && (
          <span className="text-xs px-2.5 py-1 rounded-full bg-slate-100 text-slate-500">
            +{agent.expertise.length - 3}
          </span>
        )}
      </div>

      <button
        onClick={handleChat}
        className={`mt-auto flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-colors ${colors.btn}`}
      >
        <MessageSquare size={15} />
        Discuter avec cet agent
      </button>
    </div>
  )
}
