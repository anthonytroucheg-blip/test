const BASE = import.meta.env.VITE_API_URL || ''

async function request(method, path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Erreur réseau')
  }
  if (res.status === 204) return null
  return res.json()
}

// Agents
export const getAgents = () => request('GET', '/api/agents')

// Conversations
export const getConversations = () => request('GET', '/api/conversations')
export const createConversation = (data) => request('POST', '/api/conversations', data)
export const getConversation = (id) => request('GET', `/api/conversations/${id}`)
export const deleteConversation = (id) => request('DELETE', `/api/conversations/${id}`)

// Messages
export const sendMessage = (convId, data) =>
  request('POST', `/api/conversations/${convId}/messages`, data)

// Tasks
export const getTasks = () => request('GET', '/api/tasks')
export const createTask = (data) => request('POST', '/api/tasks', data)
export const updateTask = (id, data) => request('PUT', `/api/tasks/${id}`, data)
export const deleteTask = (id) => request('DELETE', `/api/tasks/${id}`)

// Memory
export const getMemory = () => request('GET', '/api/memory')
export const createMemory = (data) => request('POST', '/api/memory', data)
export const updateMemory = (id, data) => request('PUT', `/api/memory/${id}`, data)
export const deleteMemory = (id) => request('DELETE', `/api/memory/${id}`)

// Settings
export const getSettings = () => request('GET', '/api/settings')
export const saveSettings = (data) => request('PUT', '/api/settings', data)
