import { useState, useEffect } from 'react'
import { Settings as SettingsIcon, Eye, EyeOff, Save, CheckCircle, AlertCircle } from 'lucide-react'
import { getSettings, saveSettings } from '../services/api'

const MODELS = ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-3.5-turbo']
const STYLES = [
  { value: 'professionnel', label: 'Professionnel' },
  { value: 'concis',        label: 'Concis' },
  { value: 'détaillé',     label: 'Détaillé' },
  { value: 'direct',        label: 'Direct & pragmatique' },
]

export default function Settings() {
  const [settings, setSettings] = useState({
    company_name: '',
    openai_api_key: '',
    openai_model: 'gpt-4o',
    response_style: 'professionnel',
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [status, setStatus] = useState(null) // 'saved' | 'error'
  const [showKey, setShowKey] = useState(false)
  const [apiKeyInput, setApiKeyInput] = useState('')

  useEffect(() => { load() }, [])

  async function load() {
    setLoading(true)
    try {
      const data = await getSettings()
      const map = Object.fromEntries(data.map(s => [s.key, s.value]))
      setSettings(s => ({ ...s, ...map }))
    } catch {}
    finally { setLoading(false) }
  }

  async function handleSave() {
    setSaving(true)
    setStatus(null)
    try {
      const payload = { ...settings }
      if (apiKeyInput.trim() && !apiKeyInput.includes('•')) {
        payload.openai_api_key = apiKeyInput.trim()
      }
      await saveSettings(payload)
      setStatus('saved')
      setApiKeyInput('')
      setTimeout(() => setStatus(null), 3000)
    } catch {
      setStatus('error')
    } finally {
      setSaving(false)
    }
  }

  const set = (k) => (e) => setSettings(s => ({ ...s, [k]: e.target.value }))

  if (loading) return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="space-y-4">
        {[...Array(4)].map((_, i) => <div key={i} className="h-16 bg-slate-100 rounded-2xl animate-pulse" />)}
      </div>
    </div>
  )

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-800">Paramètres</h1>
        <p className="text-slate-500 mt-1">Configuration de la plateforme et de l'API OpenAI.</p>
      </div>

      <div className="space-y-5">
        {/* Company */}
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
          <h2 className="font-semibold text-slate-800 mb-4">Général</h2>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1.5">Nom de l'entreprise</label>
            <input
              value={settings.company_name} onChange={set('company_name')}
              className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
              placeholder="Camping Saint Lambert & Vanéa"
            />
          </div>
        </div>

        {/* OpenAI */}
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
          <div className="flex items-center gap-2 mb-4">
            <h2 className="font-semibold text-slate-800">OpenAI</h2>
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
              settings.openai_api_key && !settings.openai_api_key.includes('•')
                ? 'bg-emerald-100 text-emerald-700'
                : settings.openai_api_key
                ? 'bg-emerald-100 text-emerald-700'
                : 'bg-amber-100 text-amber-700'
            }`}>
              {settings.openai_api_key ? 'Clé configurée' : 'Mode Mock — non configuré'}
            </span>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Clé API OpenAI</label>
              <div className="relative">
                <input
                  type={showKey ? 'text' : 'password'}
                  value={apiKeyInput || settings.openai_api_key}
                  onChange={(e) => setApiKeyInput(e.target.value)}
                  placeholder="sk-..."
                  className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm pr-10 focus:outline-none focus:ring-2 focus:ring-indigo-300 font-mono"
                />
                <button
                  onClick={() => setShowKey(!showKey)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                >
                  {showKey ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              <p className="text-xs text-slate-400 mt-1.5">
                Obtenez votre clé sur{' '}
                <span className="text-indigo-600 font-medium">platform.openai.com</span>.
                La clé n'est jamais affichée en clair après sauvegarde.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">Modèle</label>
                <select
                  value={settings.openai_model} onChange={set('openai_model')}
                  className="w-full border border-slate-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
                >
                  {MODELS.map(m => <option key={m} value={m}>{m}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">Style de réponse</label>
                <select
                  value={settings.response_style} onChange={set('response_style')}
                  className="w-full border border-slate-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300"
                >
                  {STYLES.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Mode mock info */}
        {!settings.openai_api_key && (
          <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex gap-3">
            <AlertCircle size={18} className="text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-amber-800">Mode démonstration actif</p>
              <p className="text-sm text-amber-700 mt-0.5">
                Les agents répondent avec des réponses pré-définies. Ajoutez votre clé API OpenAI
                pour activer les réponses IA réelles et personnalisées.
              </p>
            </div>
          </div>
        )}

        {/* Save */}
        <div className="flex items-center justify-between">
          {status === 'saved' && (
            <div className="flex items-center gap-2 text-emerald-600 text-sm font-medium">
              <CheckCircle size={16} /> Paramètres sauvegardés
            </div>
          )}
          {status === 'error' && (
            <div className="flex items-center gap-2 text-red-600 text-sm font-medium">
              <AlertCircle size={16} /> Erreur lors de la sauvegarde
            </div>
          )}
          {!status && <div />}
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white px-5 py-2.5 rounded-xl text-sm font-medium transition-colors shadow-sm"
          >
            <Save size={15} />
            {saving ? 'Sauvegarde…' : 'Sauvegarder'}
          </button>
        </div>
      </div>
    </div>
  )
}
