import { useParams } from 'react-router-dom'
import ChatWindow from '../components/ChatWindow'

export default function Chat() {
  const { convId } = useParams()
  return (
    <div className="h-full">
      <ChatWindow convId={convId} />
    </div>
  )
}
