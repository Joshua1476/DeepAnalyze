import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import apiClient from '../api/client'
import Editor from '@monaco-editor/react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import {
  Play, Send, Settings, Key, Cloud, LogOut, FileText,
  Loader, CheckCircle, XCircle, Code, Terminal
} from 'lucide-react'

export default function Dashboard() {
  const navigate = useNavigate()
  const logout = useAuthStore((state) => state.logout)
  const user = useAuthStore((state) => state.user)
  
  const [prompt, setPrompt] = useState('')
  const [projectName, setProjectName] = useState('my-project')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [ws, setWs] = useState(null)
  const [code, setCode] = useState('# Write your code here\nprint("Hello, World!")')
  const [language, setLanguage] = useState('python')
  const [output, setOutput] = useState('')
  const [activeTab, setActiveTab] = useState('chat')
  
  const messagesEndRef = useRef(null)
  
  useEffect(() => {
    // Connect WebSocket
    const websocket = new WebSocket(`ws://localhost:8000/ws/${user?.username || 'default'}`)
    
    websocket.onopen = () => {
      console.log('WebSocket connected')
    }
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setMessages((prev) => [...prev, {
        type: 'system',
        content: data.message,
        status: data.status,
        timestamp: new Date(data.timestamp)
      }])
    }
    
    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    
    websocket.onclose = () => {
      console.log('WebSocket disconnected')
    }
    
    setWs(websocket)
    
    return () => {
      websocket.close()
    }
  }, [user])
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])
  
  const handleGeneratePlan = async () => {
    if (!prompt.trim()) return
    
    setLoading(true)
    setMessages((prev) => [...prev, {
      type: 'user',
      content: prompt,
      timestamp: new Date()
    }])
    
    try {
      const response = await apiClient.post('/api/plan', {
        description: prompt,
        project_name: projectName,
        requirements: [],
        tech_stack: []
      })
      
      setMessages((prev) => [...prev, {
        type: 'assistant',
        content: `## Build Plan Generated\n\n**Project:** ${response.data.project_name}\n\n**Estimated Time:** ${response.data.estimated_time} minutes\n\n**Tech Stack:** ${response.data.tech_stack.join(', ')}\n\n### Steps:\n\n${response.data.steps.map((step, i) => `${i + 1}. **${step.title}**\n   ${step.description}\n   Files: ${step.files.join(', ')}\n   Time: ${step.estimated_minutes} min`).join('\n\n')}`,
        timestamp: new Date()
      }])
      
      setPrompt('')
    } catch (error) {
      setMessages((prev) => [...prev, {
        type: 'error',
        content: `Error: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date()
      }])
    } finally {
      setLoading(false)
    }
  }
  
  const handleExecuteCode = async () => {
    setLoading(true)
    setOutput('Executing...')
    
    try {
      const response = await apiClient.post('/api/run', {
        code,
        language,
        project_name: projectName,
        timeout: 60
      })
      
      if (response.data.success) {
        setOutput(response.data.output)
      } else {
        setOutput(`Error:\n${response.data.error}\n\nOutput:\n${response.data.output}`)
      }
    } catch (error) {
      setOutput(`Error: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }
  
  const handleLogout = () => {
    logout()
    navigate('/login')
  }
  
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              DionoAutogen AI
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Welcome, {user?.username}
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/providers')}
              className="btn btn-secondary flex items-center gap-2"
            >
              <Cloud size={20} />
              Providers
            </button>
            <button
              onClick={() => navigate('/keys')}
              className="btn btn-secondary flex items-center gap-2"
            >
              <Key size={20} />
              API Keys
            </button>
            <button
              onClick={handleLogout}
              className="btn btn-secondary flex items-center gap-2"
            >
              <LogOut size={20} />
              Logout
            </button>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('chat')}
            className={`px-4 py-2 rounded-lg font-medium ${
              activeTab === 'chat'
                ? 'bg-primary-600 text-white'
                : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300'
            }`}
          >
            <FileText className="inline mr-2" size={20} />
            Chat & Plan
          </button>
          <button
            onClick={() => setActiveTab('code')}
            className={`px-4 py-2 rounded-lg font-medium ${
              activeTab === 'code'
                ? 'bg-primary-600 text-white'
                : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300'
            }`}
          >
            <Code className="inline mr-2" size={20} />
            Code Editor
          </button>
        </div>
        
        {/* Chat Tab */}
        {activeTab === 'chat' && (
          <div className="grid grid-cols-1 gap-6">
            {/* Project Name */}
            <div className="card">
              <label className="block text-sm font-medium mb-2">Project Name</label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                className="input"
                placeholder="my-awesome-project"
              />
            </div>
            
            {/* Messages */}
            <div className="card h-96 overflow-y-auto">
              <div className="space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`p-4 rounded-lg ${
                      msg.type === 'user'
                        ? 'bg-primary-100 dark:bg-primary-900 ml-12'
                        : msg.type === 'error'
                        ? 'bg-red-100 dark:bg-red-900'
                        : 'bg-gray-100 dark:bg-gray-700 mr-12'
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      {msg.type === 'system' && <Loader className="animate-spin" size={20} />}
                      {msg.type === 'error' && <XCircle size={20} />}
                      <div className="flex-1">
                        {msg.type === 'assistant' ? (
                          <ReactMarkdown
                            components={{
                              code({ node, inline, className, children, ...props }) {
                                const match = /language-(\w+)/.exec(className || '')
                                return !inline && match ? (
                                  <SyntaxHighlighter
                                    style={vscDarkPlus}
                                    language={match[1]}
                                    PreTag="div"
                                    {...props}
                                  >
                                    {String(children).replace(/\n$/, '')}
                                  </SyntaxHighlighter>
                                ) : (
                                  <code className={className} {...props}>
                                    {children}
                                  </code>
                                )
                              }
                            }}
                          >
                            {msg.content}
                          </ReactMarkdown>
                        ) : (
                          <p className="whitespace-pre-wrap">{msg.content}</p>
                        )}
                        <p className="text-xs text-gray-500 mt-2">
                          {msg.timestamp.toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
            </div>
            
            {/* Input */}
            <div className="card">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="input min-h-32"
                placeholder="Describe what you want to build... (e.g., 'Create a REST API for a todo app with user authentication')"
                disabled={loading}
              />
              <button
                onClick={handleGeneratePlan}
                disabled={loading || !prompt.trim()}
                className="btn btn-primary w-full mt-4 flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader className="animate-spin" size={20} />
                    Generating...
                  </>
                ) : (
                  <>
                    <Send size={20} />
                    Generate Plan
                  </>
                )}
              </button>
            </div>
          </div>
        )}
        
        {/* Code Tab */}
        {activeTab === 'code' && (
          <div className="grid grid-cols-2 gap-6">
            {/* Editor */}
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">Code Editor</h3>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="input w-40"
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="typescript">TypeScript</option>
                  <option value="java">Java</option>
                  <option value="go">Go</option>
                  <option value="rust">Rust</option>
                </select>
              </div>
              <Editor
                height="500px"
                language={language}
                value={code}
                onChange={(value) => setCode(value || '')}
                theme="vs-dark"
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                }}
              />
              <button
                onClick={handleExecuteCode}
                disabled={loading}
                className="btn btn-primary w-full mt-4 flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader className="animate-spin" size={20} />
                    Executing...
                  </>
                ) : (
                  <>
                    <Play size={20} />
                    Run Code
                  </>
                )}
              </button>
            </div>
            
            {/* Output */}
            <div className="card">
              <div className="flex items-center gap-2 mb-4">
                <Terminal size={20} />
                <h3 className="text-lg font-semibold">Output</h3>
              </div>
              <pre className="bg-gray-900 text-green-400 p-4 rounded-lg h-[500px] overflow-auto font-mono text-sm">
                {output || 'Output will appear here...'}
              </pre>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
