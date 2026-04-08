import { useState, useRef, useEffect } from 'react'
import './App.css'

function App() {
  const [intent, setIntent] = useState('')
  const [events, setEvents] = useState([])
  const [isProcessing, setIsProcessing] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [events])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!intent.trim() || isProcessing) return

    setEvents([])
    setIsProcessing(true)

    try {
      const response = await fetch('http://localhost:8080/api/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ intent })
      })

      if (!response.body) throw new Error('ReadableStream not supported in this browser.')

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { value, done } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split('\n\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.replace('data: ', '')
            if (dataStr.trim()) {
              try {
                const parsed = JSON.parse(dataStr)
                if (parsed.type === 'end') {
                   setIsProcessing(false)
                } else {
                   setEvents(prev => [...prev, parsed])
                }
              } catch (err) {
                console.error('Error parsing SSE:', err)
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Error submitting intent:', error)
      setIsProcessing(false)
    }
  }

  const getAgentColor = (agentName) => {
    if (agentName.includes("Context")) return "agent-context"
    if (agentName.includes("Planning")) return "agent-planning"
    if (agentName.includes("Scheduling")) return "agent-scheduling"
    if (agentName.includes("Execution")) return "agent-execution"
    return "agent-system"
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>LifeOS <span className="highlight">AI</span></h1>
        <p className="subtitle">Your autonomous multi-agent chief of staff.</p>
      </header>

      <main className="main-content">
        <form onSubmit={handleSubmit} className="input-form">
          <input 
            type="text" 
            placeholder='e.g., "Plan my next 4 hours" or "I just lost 2 hours"'
            value={intent}
            onChange={(e) => setIntent(e.target.value)}
            disabled={isProcessing}
            className="intent-input"
          />
          <button type="submit" disabled={isProcessing || !intent.trim()} className="exec-button">
             {isProcessing ? 'Thinking...' : 'Execute'}
          </button>
        </form>

        <section className="events-container">
          {events.length === 0 && !isProcessing && (
            <div className="empty-state">
               Systems online. Awaiting cognitive input...
            </div>
          )}
          {events.map((ev, idx) => (
            <div key={idx} className={`event-card ${getAgentColor(ev.agent)} slide-in ${ev.type}`}>
               <div className="event-header">
                 <span className="agent-badge">{ev.agent}</span>
                 <span className={`status-icon ${ev.status}`}></span>
               </div>
               <div className="event-body">
                 {ev.type === 'thought' ? (
                    <p className="thought-text"><span className="pulse">●</span> {ev.content}</p>
                 ) : (
                    <p className="action-text">{ev.content}</p>
                 )}
               </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </section>
      </main>
    </div>
  )
}

export default App
