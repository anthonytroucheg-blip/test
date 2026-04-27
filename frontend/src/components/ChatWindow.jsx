import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Send, Plus, Trash2, Network, TrendingUp, Tent, MapPin, Zap, Target, Bot } from 'lucide-react'
import { getConversations, createConversation, getConversation, sendMessage, deleteConversation } from '../services/api'

const AGENT_META = {
  orchestrateur: { label: 'Chef d\'Orchestre', icon: Network, color: 'bg-indigo-600' },
  finance:       { label: 'Finance',           icon: TrendingUp, color: 'bg-emerald-600' },
  camping:       { label: 'Camping',           icon: Tent,       color: 'bg-amber-500' },
  vanea:         { label: 'Vanéa',             icon: MapPin,     color: 'bg-blue-600' },
  operations:    { label: 'Opérations',        icon: Zap,        color: 'bg-orange-500' },
  strategie:     { label: 'Stratégie',         icon: Target,     color: 'bg-violet-600' },
}

function AgentBadge({ agentId }) {
  const meta = AGENT_META[agentId] || { label: agentId, color: 'bg-slate-600' }
  const Icon = meta.icon || Bot
  return (
    <span className={`inline-flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-full text-white ${meta.color}`}>
      <Icon size={10} />
      {meta.label}
    </span>
  )
}

export default function ChatWindow({ convId, onConvChange }) {
  const navigate = useNavigate()
  const [conversations, setConversations] = useState([])
  const [activeConv, setActiveConv] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedAgent, setSelectedAgent] = useState('orchestrateur')
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    loadConversations()
  }, [])

  useEffect(() => {
    if (convId) loadConversation(convId)
    else { setActiveConv(null); setMessages([]) }
  }, [convId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function loadConversations() {
    try { setConversations(await getConversations()) } catch {}
  }

  async function loadConversation(id) {
    try {
      const conv = await getConversation(id)
      setActiveConv(conv)
      setMessages(conv.messages || [])
      setSelectedAgent(conv.agent_id || 'orchestrateur')
    } catch { navigate('/chat') }
  }

  async function handleNewConv() {
    try {
      const conv = await createConversation({ agent_id: selectedAgent })
      await loadConversations()
      navigate(`/chat/${conv.id}`)
    } catch {}
  }

  async function handleDelete(id) {
    try {
      await deleteConversation(id)
      await loadConversations()
      if (convId === id) navigate('/chat')
    } catch {}
  }

  async function handleSend() {
    const content = input.trim()
    if (!content || loading) return

    if (!convId) {
      try {
        const conv = await createConversation({ agent_id: selectedAgent })
        navigate(`/chat/${conv.id}`)
        setTimeout(() => handleSendToConv(conv.id, content), 100)
      } catch {}
      return
    }
    handleSendToConv(convId, content)
  }

  async function handleSendToConv(id, content) {
    setInput('')
    setLoading(true)
    const optimistic = { id: 'temp', role: 'user', content, agent_id: null, created_at: new Date() }
    setMessages(prev => [...prev, optimistic])

    try {
      const { user_message, assistant_message } = await sendMessage(id, {
        content,
        agent_id: selectedAgent,
      })
      setMessages(prev => [...prev.filter(m => m.id !== 'temp'), user_message, assistant_message])
      await loadConversations()
    } catch (e) {
      setMessages(prev => prev.filter(m => m.id !== 'temp'))
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex h-full">
      {/* Conversation list */}
      <aside className="hidden lg:flex w-64 flex-col bg-white border-r border-slate-100 flex-shrink-0">
        <div className="p-4 border-b border-slate-100 flex items-center justify-between">
          <h2 className="font-semibold text-slate-800 text-sm">Conversations</h2>
          <button
            onClick={handleNewConv}
            className="p-1.5 rounded-lg bg-indigo-50 text-indigo-600 hover:bg-indigo-100 transition-colors"
            title="Nouvelle conversation"
          >
            <Plus size={16} />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-0.5">
          {conversations.length === 0 && (
            <p className="text-xs text-slate-400 text-center py-6 px-3">
              Aucune conversation.<br />Commencez à écrire.
            </p>
          )}
          {conversations.map((c) => {
            const meta = AGENT_META[c.agent_id]
            return (
              <div
                key={c.id}
                onClick={() => navigate(`/chat/${c.id}`)}
                className={`group flex items-center gap-2 px-3 py-2.5 rounded-lg cursor-pointer transition-colors ${
                  convId === c.id ? 'bg-indigo-50 border border-indigo-100' : 'hover:bg-slate-50'
                }`}
              >
                {meta && (
                  <div className={`w-5 h-5 rounded flex items-center justify-center flex-shrink-0 text-white ${meta.color}`}>
                    <meta.icon size={11} />
                  </div>
                )}
                <p className={`flex-1 text-xs truncate ${convId === c.id ? 'text-indigo-700 font-medium' : 'text-slate-700'}`}>
                  {c.title}
                </p>
                <button
                  onClick={(e) => { e.stopPropagation(); handleDelete(c.id) }}
                  className="opacity-0 group-hover:opacity-100 p-1 rounded hover:text-red-500 text-slate-400 transition-all"
                >
                  <Trash2 size={12} />
                </button>
              </div>
            )
          })}
        </div>
      </aside>

      {/* Chat area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <div className="bg-white border-b border-slate-100 px-6 py-3 flex items-center gap-3 flex-shrink-0">
          <div className="flex-1 min-w-0">
            <h1 className="font-semibold text-slate-800 text-sm truncate">
              {activeConv ? activeConv.title : 'Nouveau chat'}
            </h1>
          </div>
          {/* Agent selector */}
          <select
            value={selectedAgent}
            onChange={(e) => setSelectedAgent(e.target.value)}
            className="text-xs border border-slate-200 rounded-lg px-2.5 py-1.5 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-300"
          >
            {Object.entries(AGENT_META).map(([id, m]) => (
              <option key={id} value={id}>{m.label}</option>
            ))}
          </select>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
          {messages.length === 0 && !loading && (
            <div className="h-full flex flex-col items-center justify-center text-center py-16">
              <div className="w-14 h-14 bg-indigo-100 rounded-2xl flex items-center justify-center mb-4">
                <Network size={28} className="text-indigo-600" />
              </div>
              <h3 className="font-semibold text-slate-700 mb-2">Votre équipe IA est prête</h3>
              <p className="text-sm text-slate-400 max-w-xs">
                Posez une question ou donnez une tâche au Chef d'Orchestre.
                Il mobilisera les agents spécialisés pour vous.
              </p>
              <div className="mt-6 grid grid-cols-1 gap-2 w-full max-w-sm">
                {[
                  'Prépare mes priorités de la semaine',
                  'Analyse la rentabilité de Vanéa',
                  'Crée une procédure ménage pour les mobil-homes',
                ].map(s => (
                  <button
                    key={s}
                    onClick={() => setInput(s)}
                    className="text-left text-xs px-3 py-2 rounded-lg bg-white border border-slate-200 text-slate-600 hover:border-indigo-300 hover:text-indigo-700 transition-colors"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.role === 'user' ? (
                <div className="max-w-[75%] bg-indigo-600 text-white text-sm px-4 py-3 rounded-2xl rounded-br-sm shadow-sm">
                  {msg.content}
                </div>
              ) : (
                <div className="max-w-[85%] flex flex-col gap-1.5">
                  {msg.agent_id && <AgentBadge agentId={msg.agent_id} />}
                  <div className="bg-white border border-slate-100 shadow-sm rounded-2xl rounded-tl-sm px-4 py-3">
                    <div className="prose-chat">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-white border border-slate-100 shadow-sm rounded-2xl rounded-tl-sm px-4 py-3">
                <div className="flex gap-1.5 items-center">
                  <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="bg-white border-t border-slate-100 px-4 py-3 flex-shrink-0">
          <div className="flex gap-2 items-end">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Écrivez votre message… (Entrée pour envoyer, Maj+Entrée pour nouvelle ligne)"
              rows={1}
              className="flex-1 resize-none border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-transparent max-h-32 overflow-y-auto"
              style={{ minHeight: '42px' }}
              onInput={(e) => {
                e.target.style.height = 'auto'
                e.target.style.height = Math.min(e.target.scrollHeight, 128) + 'px'
              }}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="p-2.5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-200 disabled:text-slate-400 text-white rounded-xl transition-colors flex-shrink-0"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
