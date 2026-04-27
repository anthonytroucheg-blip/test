import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { MessageSquare, CheckSquare, Users, Sparkles, ArrowRight, Plus } from 'lucide-react'
import DashboardCard from '../components/DashboardCard'
import AgentCard from '../components/AgentCard'
import { getConversations, getTasks, getAgents, createConversation } from '../services/api'

const SUGGESTIONS = [
  { text: 'Prépare mes priorités de la semaine', agent: 'operations' },
  { text: 'Analyse la rentabilité de Vanéa', agent: 'finance' },
  { text: 'Rédige une réponse à un client mécontent', agent: 'camping' },
  { text: 'Crée une procédure ménage pour les mobil-homes', agent: 'camping' },
  { text: 'Plan marketing Camping Saint Lambert', agent: 'strategie' },
  { text: 'Aide-moi à décider d\'un investissement', agent: 'finance' },
]

export default function Dashboard() {
  const navigate = useNavigate()
  const [conversations, setConversations] = useState([])
  const [tasks, setTasks] = useState([])
  const [agents, setAgents] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getConversations(), getTasks(), getAgents()])
      .then(([c, t, a]) => { setConversations(c); setTasks(t); setAgents(a) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const activeTasks = tasks.filter(t => t.status !== 'done')
  const recentConvs = conversations.slice(0, 4)

  async function startSuggestion(s) {
    const conv = await createConversation({ agent_id: s.agent })
    navigate(`/chat/${conv.id}`, { state: { initialMessage: s.text } })
  }

  const today = new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <p className="text-sm text-slate-400 capitalize mb-1">{today}</p>
        <h1 className="text-2xl font-bold text-slate-800">Bonjour 👋</h1>
        <p className="text-slate-500 mt-1">Votre équipe IA est prête à vous aider.</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <DashboardCard icon={Users} label="Agents actifs" value={agents.length || 6} color="indigo" />
        <DashboardCard icon={MessageSquare} label="Conversations" value={conversations.length} sub="total" color="violet" />
        <DashboardCard icon={CheckSquare} label="Tâches actives" value={activeTasks.length} sub={`/ ${tasks.length} total`} color="amber" />
        <DashboardCard icon={Sparkles} label="Mode IA" value="Mock" sub="Configurez l'API OpenAI" color="emerald" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Suggestions */}
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-slate-800">Suggestions d'actions</h2>
              <Sparkles size={16} className="text-indigo-400" />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s.text}
                  onClick={() => startSuggestion(s)}
                  className="text-left px-3 py-3 rounded-xl border border-slate-100 hover:border-indigo-200 hover:bg-indigo-50 text-sm text-slate-600 hover:text-indigo-700 transition-all group flex items-center gap-2"
                >
                  <span className="flex-1">{s.text}</span>
                  <ArrowRight size={14} className="opacity-0 group-hover:opacity-100 transition-opacity text-indigo-500 flex-shrink-0" />
                </button>
              ))}
            </div>
          </div>

          {/* Recent conversations */}
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-slate-800">Conversations récentes</h2>
              <button onClick={() => navigate('/chat')} className="text-xs text-indigo-600 hover:underline">Voir tout</button>
            </div>
            {recentConvs.length === 0 ? (
              <div className="text-center py-6">
                <p className="text-sm text-slate-400">Aucune conversation pour l'instant.</p>
                <button onClick={() => navigate('/chat')} className="mt-2 text-sm text-indigo-600 hover:underline">Commencer →</button>
              </div>
            ) : (
              <div className="space-y-2">
                {recentConvs.map(c => (
                  <button
                    key={c.id}
                    onClick={() => navigate(`/chat/${c.id}`)}
                    className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-slate-50 text-left transition-colors group"
                  >
                    <div className="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center flex-shrink-0">
                      <MessageSquare size={14} className="text-indigo-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-700 truncate">{c.title}</p>
                      <p className="text-xs text-slate-400">
                        {new Date(c.updated_at).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })}
                      </p>
                    </div>
                    <ArrowRight size={14} className="text-slate-300 group-hover:text-indigo-500 transition-colors flex-shrink-0" />
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right column */}
        <div className="space-y-6">
          {/* Tasks preview */}
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-slate-800">Tâches en cours</h2>
              <button onClick={() => navigate('/tasks')} className="text-xs text-indigo-600 hover:underline">Voir tout</button>
            </div>
            {activeTasks.length === 0 ? (
              <div className="text-center py-4">
                <p className="text-sm text-slate-400 mb-2">Aucune tâche active.</p>
                <button onClick={() => navigate('/tasks')} className="text-xs text-indigo-600 hover:underline flex items-center gap-1 mx-auto">
                  <Plus size={12} /> Ajouter une tâche
                </button>
              </div>
            ) : (
              <div className="space-y-2">
                {activeTasks.slice(0, 4).map(t => (
                  <div key={t.id} className="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-slate-50">
                    <div className={`w-2 h-2 rounded-full flex-shrink-0 ${
                      t.priority === 'high' ? 'bg-red-500' : t.priority === 'medium' ? 'bg-amber-500' : 'bg-emerald-500'
                    }`} />
                    <p className="text-sm text-slate-600 truncate flex-1">{t.title}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Agents preview */}
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-slate-800">Agents disponibles</h2>
              <button onClick={() => navigate('/agents')} className="text-xs text-indigo-600 hover:underline">Voir tout</button>
            </div>
            <div className="space-y-2">
              {agents.slice(0, 4).map(a => (
                <AgentCard key={a.id} agent={a} compact />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
