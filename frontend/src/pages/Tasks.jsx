import { useState, useEffect } from 'react'
import { Plus, Trash2, CheckCircle, Circle, Clock, AlertCircle } from 'lucide-react'
import { getTasks, createTask, updateTask, deleteTask } from '../services/api'

const PRIORITY_CONFIG = {
  high:   { label: 'Haute',   color: 'text-red-600 bg-red-50 border-red-100' },
  medium: { label: 'Moyenne', color: 'text-amber-600 bg-amber-50 border-amber-100' },
  low:    { label: 'Basse',   color: 'text-emerald-600 bg-emerald-50 border-emerald-100' },
}

const STATUS_CONFIG = {
  todo:        { label: 'À faire',   icon: Circle,       color: 'text-slate-400' },
  in_progress: { label: 'En cours',  icon: Clock,        color: 'text-amber-500' },
  done:        { label: 'Terminé',   icon: CheckCircle,  color: 'text-emerald-500' },
}

const AGENT_LABELS = {
  orchestrateur: 'Chef d\'Orchestre',
  finance: 'Finance', camping: 'Camping',
  vanea: 'Vanéa', operations: 'Opérations', strategie: 'Stratégie',
}

function Modal({ onClose, onSave }) {
  const [form, setForm] = useState({ title: '', description: '', priority: 'medium', status: 'todo', agent_id: '' })
  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6" onClick={e => e.stopPropagation()}>
        <h2 className="font-semibold text-slate-800 text-lg mb-4">Nouvelle tâche</h2>
        <div className="space-y-3">
          <input
            value={form.title} onChange={set('title')} placeholder="Titre de la tâche *"
            className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
          />
          <textarea
            value={form.description} onChange={set('description')} placeholder="Description (optionnel)"
            rows={3}
            className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 resize-none"
          />
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-slate-500 mb-1 block">Priorité</label>
              <select value={form.priority} onChange={set('priority')}
                className="w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300">
                <option value="high">Haute</option>
                <option value="medium">Moyenne</option>
                <option value="low">Basse</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-slate-500 mb-1 block">Statut</label>
              <select value={form.status} onChange={set('status')}
                className="w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300">
                <option value="todo">À faire</option>
                <option value="in_progress">En cours</option>
                <option value="done">Terminé</option>
              </select>
            </div>
          </div>
          <div>
            <label className="text-xs text-slate-500 mb-1 block">Agent concerné</label>
            <select value={form.agent_id} onChange={set('agent_id')}
              className="w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300">
              <option value="">Aucun</option>
              {Object.entries(AGENT_LABELS).map(([id, label]) => (
                <option key={id} value={id}>{label}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="flex gap-3 mt-5">
          <button onClick={onClose} className="flex-1 border border-slate-200 rounded-xl py-2.5 text-sm text-slate-600 hover:bg-slate-50 transition-colors">
            Annuler
          </button>
          <button
            onClick={() => form.title.trim() && onSave(form)}
            className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl py-2.5 text-sm font-medium transition-colors"
          >
            Créer
          </button>
        </div>
      </div>
    </div>
  )
}

export default function Tasks() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    load()
  }, [])

  async function load() {
    setLoading(true)
    try { setTasks(await getTasks()) } catch {} finally { setLoading(false) }
  }

  async function handleCreate(data) {
    try {
      const task = await createTask(data)
      setTasks(prev => [task, ...prev])
      setShowModal(false)
    } catch {}
  }

  async function handleStatus(task, status) {
    try {
      const updated = await updateTask(task.id, { status })
      setTasks(prev => prev.map(t => t.id === task.id ? updated : t))
    } catch {}
  }

  async function handleDelete(id) {
    try {
      await deleteTask(id)
      setTasks(prev => prev.filter(t => t.id !== id))
    } catch {}
  }

  const filtered = tasks.filter(t => filter === 'all' || t.status === filter)
  const counts = {
    all: tasks.length,
    todo: tasks.filter(t => t.status === 'todo').length,
    in_progress: tasks.filter(t => t.status === 'in_progress').length,
    done: tasks.filter(t => t.status === 'done').length,
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      {showModal && <Modal onClose={() => setShowModal(false)} onSave={handleCreate} />}

      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Tâches</h1>
          <p className="text-slate-500 mt-0.5">{tasks.length} tâche{tasks.length > 1 ? 's' : ''} au total</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2.5 rounded-xl text-sm font-medium transition-colors shadow-sm"
        >
          <Plus size={16} /> Nouvelle tâche
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-2 mb-5">
        {[
          ['all', 'Toutes'],
          ['todo', 'À faire'],
          ['in_progress', 'En cours'],
          ['done', 'Terminées'],
        ].map(([key, label]) => (
          <button
            key={key}
            onClick={() => setFilter(key)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              filter === key
                ? 'bg-indigo-600 text-white'
                : 'bg-white border border-slate-200 text-slate-600 hover:border-indigo-300'
            }`}
          >
            {label} <span className="ml-1 opacity-70">({counts[key]})</span>
          </button>
        ))}
      </div>

      {/* Task list */}
      {loading ? (
        <div className="space-y-3">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-20 bg-slate-100 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-slate-100">
          <AlertCircle size={40} className="mx-auto text-slate-200 mb-3" />
          <p className="text-slate-500">Aucune tâche dans cette catégorie.</p>
          <button onClick={() => setShowModal(true)} className="mt-2 text-sm text-indigo-600 hover:underline flex items-center gap-1 mx-auto">
            <Plus size={14} /> Créer une tâche
          </button>
        </div>
      ) : (
        <div className="space-y-2">
          {filtered.map(task => {
            const pCfg = PRIORITY_CONFIG[task.priority] || PRIORITY_CONFIG.medium
            const sCfg = STATUS_CONFIG[task.status] || STATUS_CONFIG.todo
            const StatusIcon = sCfg.icon
            return (
              <div key={task.id}
                className="bg-white border border-slate-100 rounded-2xl px-5 py-4 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow group">
                <button onClick={() => handleStatus(task, task.status === 'done' ? 'todo' : 'done')}
                  className={`flex-shrink-0 transition-colors ${sCfg.color} hover:scale-110`}>
                  <StatusIcon size={20} />
                </button>

                <div className="flex-1 min-w-0">
                  <p className={`font-medium text-sm ${task.status === 'done' ? 'line-through text-slate-400' : 'text-slate-800'}`}>
                    {task.title}
                  </p>
                  {task.description && (
                    <p className="text-xs text-slate-400 mt-0.5 truncate">{task.description}</p>
                  )}
                  <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                    <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${pCfg.color}`}>
                      {pCfg.label}
                    </span>
                    {task.agent_id && (
                      <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">
                        {AGENT_LABELS[task.agent_id] || task.agent_id}
                      </span>
                    )}
                    <span className="text-xs text-slate-400">
                      {new Date(task.created_at).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  {task.status !== 'in_progress' && (
                    <button onClick={() => handleStatus(task, 'in_progress')}
                      className="p-1.5 rounded-lg text-amber-500 hover:bg-amber-50 text-xs transition-colors"
                      title="Marquer en cours">
                      <Clock size={14} />
                    </button>
                  )}
                  <button onClick={() => handleDelete(task.id)}
                    className="p-1.5 rounded-lg text-red-400 hover:bg-red-50 transition-colors">
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
