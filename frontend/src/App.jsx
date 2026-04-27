import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Agents from './pages/Agents'
import Chat from './pages/Chat'
import Tasks from './pages/Tasks'
import Memory from './pages/Memory'
import Settings from './pages/Settings'

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen overflow-hidden bg-slate-50">
        <Sidebar />
        <main className="flex-1 overflow-auto min-w-0">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/chat/:convId" element={<Chat />} />
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/memory" element={<Memory />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
