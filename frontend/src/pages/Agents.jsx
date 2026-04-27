import { useState, useEffect } from 'react'
import { Users, Sparkles } from 'lucide-react'
import AgentCard from '../components/AgentCard'
import { getAgents } from '../services/api'

export default function Agents() {
  const [agents, setAgents] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getAgents().then(setAgents).catch(() => {}).finally(() => setLoading(false))
  }, [])

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-8 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 mb-1">Équipe IA</h1>
          <p className="text-slate-500">
            {agents.length} agents spécialisés à votre service
          </p>
        </div>
        <div className="flex items-center gap-2 bg-indigo-50 text-indigo-700 text-sm px-3 py-2 rounded-xl border border-indigo-100">
          <Sparkles size={15} />
          <span className="font-medium">Mode Mock actif</span>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-64 bg-slate-100 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : (
        <>
          {/* Orchestrateur featured */}
          {agents.filter(a => a.id === 'orchestrateur').map(a => (
            <div key={a.id} className="mb-6">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Chef d'Orchestre</p>
              <div className="max-w-md">
                <AgentCard agent={a} />
              </div>
            </div>
          ))}

          {/* Specialists */}
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Agents spécialisés</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {agents.filter(a => a.id !== 'orchestrateur').map(a => (
                <AgentCard key={a.id} agent={a} />
              ))}
            </div>
          </div>
        </>
      )}

      {/* Info banner */}
      <div className="mt-8 bg-gradient-to-r from-indigo-50 to-violet-50 border border-indigo-100 rounded-2xl p-5">
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
            <Sparkles size={15} className="text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-indigo-900 mb-1">Activer les réponses IA réelles</h3>
            <p className="text-sm text-indigo-700">
              Actuellement en mode démonstration. Ajoutez votre clé API OpenAI dans les{' '}
              <a href="/settings" className="underline font-medium">Paramètres</a>{' '}
              pour obtenir des réponses intelligentes et personnalisées à votre situation réelle.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
