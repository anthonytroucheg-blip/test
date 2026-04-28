import { useState, useEffect, useRef } from 'react'
import { Plus, Edit2, Trash2, Brain, X, Check, Upload, FileText, Loader2 } from 'lucide-react'
import { getMemory, createMemory, updateMemory, deleteMemory, uploadDocument } from '../services/api'

const CATEGORIES = [
  { id: 'all',         label: 'Tout',         color: 'slate' },
  { id: 'camping',     label: 'Camping',      color: 'amber' },
  { id: 'vanea',       label: 'Vanéa',        color: 'blue' },
  { id: 'objectives',  label: 'Objectifs',    color: 'emerald' },
  { id: 'constraints', label: 'Contraintes',  color: 'red' },
  { id: 'notes',       label: 'Notes',        color: 'violet' },
]

const CAT_COLORS = {
  camping:     'bg-amber-50 border-amber-200 text-amber-700',
  vanea:       'bg-blue-50 border-blue-200 text-blue-700',
  objectives:  'bg-emerald-50 border-emerald-200 text-emerald-700',
  constraints: 'bg-red-50 border-red-200 text-red-700',
  notes:       'bg-violet-50 border-violet-200 text-violet-700',
}

function MemoryModal({ item, onClose, onSave }) {
  const [form, setForm] = useState(
    item ? { ...item } : { category: 'notes', title: '', content: '' }
  )
  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-slate-800 text-lg">
            {item ? 'Modifier' : 'Ajouter une information'}
          </h2>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-100 text-slate-400">
            <X size={18} />
          </button>
        </div>
        <div className="space-y-3">
          <div>
            <label className="text-xs text-slate-500 mb-1 block">Catégorie</label>
            <select value={form.category} onChange={set('category')}
              className="w-full border border-slate-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300">
              {CATEGORIES.filter(c => c.id !== 'all').map(c => (
                <option key={c.id} value={c.id}>{c.label}</option>
              ))}
            </select>
          </div>
          <input
            value={form.title} onChange={set('title')} placeholder="Titre *"
            className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
          />
          <textarea
            value={form.content} onChange={set('content')} placeholder="Contenu *"
            rows={6}
            className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 resize-none"
          />
        </div>
        <div className="flex gap-3 mt-5">
          <button onClick={onClose} className="flex-1 border border-slate-200 rounded-xl py-2.5 text-sm text-slate-600 hover:bg-slate-50">
            Annuler
          </button>
          <button
            onClick={() => form.title.trim() && form.content.trim() && onSave(form)}
            className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl py-2.5 text-sm font-medium"
          >
            {item ? 'Enregistrer' : 'Ajouter'}
          </button>
        </div>
      </div>
    </div>
  )
}

function UploadModal({ onClose, onUploaded }) {
  const [file, setFile] = useState(null)
  const [category, setCategory] = useState('notes')
  const [title, setTitle] = useState('')
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const inputRef = useRef()

  const handleFile = (f) => {
    setFile(f)
    if (!title) setTitle(f.name.replace(/\.[^.]+$/, ''))
    setError('')
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }

  async function submit() {
    if (!file) return
    setUploading(true)
    setError('')
    try {
      const result = await uploadDocument(file, category, title)
      onUploaded(result)
      onClose()
    } catch (e) {
      setError(e.message)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-slate-800 text-lg flex items-center gap-2">
            <Upload size={18} className="text-indigo-500" /> Importer un document
          </h2>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-100 text-slate-400"><X size={18} /></button>
        </div>

        <div
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors mb-4 ${file ? 'border-indigo-300 bg-indigo-50' : 'border-slate-200 hover:border-indigo-300 hover:bg-slate-50'}`}
          onClick={() => inputRef.current.click()}
          onDrop={handleDrop}
          onDragOver={e => e.preventDefault()}
        >
          <input ref={inputRef} type="file" accept=".pdf,.docx,.txt,.md" className="hidden" onChange={e => e.target.files[0] && handleFile(e.target.files[0])} />
          {file ? (
            <div className="flex items-center justify-center gap-2 text-indigo-600">
              <FileText size={20} />
              <span className="text-sm font-medium">{file.name}</span>
              <span className="text-xs text-slate-400">({(file.size / 1024).toFixed(0)} Ko)</span>
            </div>
          ) : (
            <>
              <Upload size={28} className="mx-auto text-slate-300 mb-2" />
              <p className="text-sm text-slate-500">Glisse un fichier ici ou <span className="text-indigo-600">clique pour choisir</span></p>
              <p className="text-xs text-slate-400 mt-1">PDF, DOCX, TXT — max 10 Mo</p>
            </>
          )}
        </div>

        <div className="space-y-3">
          <div>
            <label className="text-xs text-slate-500 mb-1 block">Catégorie</label>
            <select value={category} onChange={e => setCategory(e.target.value)}
              className="w-full border border-slate-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300">
              {CATEGORIES.filter(c => c.id !== 'all').map(c => (
                <option key={c.id} value={c.id}>{c.label}</option>
              ))}
            </select>
          </div>
          <input
            value={title} onChange={e => setTitle(e.target.value)} placeholder="Titre (optionnel)"
            className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
          />
        </div>

        {error && <p className="text-xs text-red-500 mt-3 bg-red-50 rounded-lg px-3 py-2">{error}</p>}

        <div className="flex gap-3 mt-5">
          <button onClick={onClose} className="flex-1 border border-slate-200 rounded-xl py-2.5 text-sm text-slate-600 hover:bg-slate-50">
            Annuler
          </button>
          <button
            onClick={submit}
            disabled={!file || uploading}
            className="flex-1 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl py-2.5 text-sm font-medium flex items-center justify-center gap-2"
          >
            {uploading ? <><Loader2 size={15} className="animate-spin" /> Traitement…</> : <><Upload size={15} /> Importer</>}
          </button>
        </div>
      </div>
    </div>
  )
}

export default function Memory() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const [modal, setModal] = useState(null) // null | 'new' | { item }
  const [uploadOpen, setUploadOpen] = useState(false)

  useEffect(() => { load() }, [])

  async function load() {
    setLoading(true)
    try { setItems(await getMemory()) } catch {} finally { setLoading(false) }
  }

  function handleUploaded(item) {
    setItems(prev => [item, ...prev])
  }

  async function handleSave(data) {
    try {
      if (modal?.item) {
        const updated = await updateMemory(modal.item.id, data)
        setItems(prev => prev.map(i => i.id === modal.item.id ? updated : i))
      } else {
        const created = await createMemory(data)
        setItems(prev => [created, ...prev])
      }
      setModal(null)
    } catch {}
  }

  async function handleDelete(id) {
    try {
      await deleteMemory(id)
      setItems(prev => prev.filter(i => i.id !== id))
    } catch {}
  }

  const filtered = items.filter(i => filter === 'all' || i.category === filter)

  return (
    <div className="p-6 max-w-5xl mx-auto">
      {modal !== null && (
        <MemoryModal
          item={modal === 'new' ? null : modal.item}
          onClose={() => setModal(null)}
          onSave={handleSave}
        />
      )}
      {uploadOpen && (
        <UploadModal onClose={() => setUploadOpen(false)} onUploaded={handleUploaded} />
      )}

      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Mémoire & Contexte</h1>
          <p className="text-slate-500 mt-0.5">
            Ces informations sont transmises aux agents IA pour personnaliser leurs réponses.
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setUploadOpen(true)}
            className="flex items-center gap-2 bg-white border border-slate-200 hover:border-indigo-300 text-slate-700 hover:text-indigo-600 px-4 py-2.5 rounded-xl text-sm font-medium shadow-sm transition-colors"
          >
            <Upload size={16} /> Importer
          </button>
          <button
            onClick={() => setModal('new')}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2.5 rounded-xl text-sm font-medium shadow-sm"
          >
            <Plus size={16} /> Ajouter
          </button>
        </div>
      </div>

      {/* Category filters */}
      <div className="flex flex-wrap gap-2 mb-6">
        {CATEGORIES.map(cat => (
          <button
            key={cat.id}
            onClick={() => setFilter(cat.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              filter === cat.id
                ? 'bg-indigo-600 text-white'
                : 'bg-white border border-slate-200 text-slate-600 hover:border-indigo-300'
            }`}
          >
            {cat.label}
            {cat.id !== 'all' && (
              <span className="ml-1 opacity-60">
                ({items.filter(i => i.category === cat.id).length})
              </span>
            )}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[...Array(4)].map((_, i) => <div key={i} className="h-40 bg-slate-100 rounded-2xl animate-pulse" />)}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-slate-100">
          <Brain size={40} className="mx-auto text-slate-200 mb-3" />
          <p className="text-slate-500 mb-2">Aucune information dans cette catégorie.</p>
          <button onClick={() => setModal('new')} className="text-sm text-indigo-600 hover:underline flex items-center gap-1 mx-auto">
            <Plus size={14} /> Ajouter une information
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map(item => {
            const catColors = CAT_COLORS[item.category] || 'bg-slate-50 border-slate-200 text-slate-600'
            return (
              <div key={item.id} className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow group">
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div className="flex-1 min-w-0">
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full border inline-block mb-2 ${catColors}`}>
                      {CATEGORIES.find(c => c.id === item.category)?.label || item.category}
                    </span>
                    <h3 className="font-semibold text-slate-800 text-sm leading-tight">{item.title}</h3>
                  </div>
                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0">
                    <button
                      onClick={() => setModal({ item })}
                      className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-indigo-600 transition-colors"
                    >
                      <Edit2 size={14} />
                    </button>
                    <button
                      onClick={() => handleDelete(item.id)}
                      className="p-1.5 rounded-lg hover:bg-red-50 text-slate-400 hover:text-red-500 transition-colors"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
                <p className="text-sm text-slate-600 whitespace-pre-line leading-relaxed">{item.content}</p>
                <p className="text-xs text-slate-300 mt-3">
                  Modifié le {new Date(item.updated_at).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })}
                </p>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
