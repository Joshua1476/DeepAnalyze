import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Key, Plus, Trash2, ArrowLeft, Eye, EyeOff } from 'lucide-react'

export default function Keys() {
  const navigate = useNavigate()
  const [keys, setKeys] = useState([
    { id: 1, name: 'OpenAI API Key', service: 'openai', key: 'sk-...', created: '2024-01-15' },
  ])
  
  const [showAddModal, setShowAddModal] = useState(false)
  const [showKey, setShowKey] = useState({})
  const [newKey, setNewKey] = useState({ name: '', service: 'openai', key: '' })
  
  const handleAdd = () => {
    if (newKey.name && newKey.key) {
      setKeys([...keys, {
        id: Date.now(),
        ...newKey,
        created: new Date().toISOString().split('T')[0]
      }])
      setNewKey({ name: '', service: 'openai', key: '' })
      setShowAddModal(false)
    }
  }
  
  const handleDelete = (id) => {
    setKeys(keys.filter(k => k.id !== id))
  }
  
  const toggleShowKey = (id) => {
    setShowKey({ ...showKey, [id]: !showKey[id] })
  }
  
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-4">
          <button
            onClick={() => navigate('/')}
            className="btn btn-secondary"
          >
            <ArrowLeft size={20} />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              API Keys Management
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Manage your LLM and service API keys
            </p>
          </div>
        </div>
      </header>
      
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-6">
          <button
            onClick={() => setShowAddModal(true)}
            className="btn btn-primary flex items-center gap-2"
          >
            <Plus size={20} />
            Add New Key
          </button>
        </div>
        
        <div className="space-y-4">
          {keys.map((keyItem) => (
            <div key={keyItem.id} className="card">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 flex-1">
                  <Key size={24} className="text-primary-600" />
                  <div className="flex-1">
                    <h3 className="font-semibold">{keyItem.name}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Service: {keyItem.service}
                    </p>
                    <div className="flex items-center gap-2 mt-2">
                      <code className="bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded text-sm">
                        {showKey[keyItem.id] ? keyItem.key : '••••••••••••••••'}
                      </code>
                      <button
                        onClick={() => toggleShowKey(keyItem.id)}
                        className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100"
                      >
                        {showKey[keyItem.id] ? <EyeOff size={20} /> : <Eye size={20} />}
                      </button>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">
                      Created: {keyItem.created}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(keyItem.id)}
                  className="btn btn-secondary"
                >
                  <Trash2 size={20} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>
      
      {/* Add Key Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="card max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">Add New API Key</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  Key Name
                </label>
                <input
                  type="text"
                  className="input"
                  placeholder="e.g., OpenAI Production Key"
                  value={newKey.name}
                  onChange={(e) => setNewKey({ ...newKey, name: e.target.value })}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">
                  Service
                </label>
                <select
                  className="input"
                  value={newKey.service}
                  onChange={(e) => setNewKey({ ...newKey, service: e.target.value })}
                >
                  <option value="openai">OpenAI</option>
                  <option value="anthropic">Anthropic</option>
                  <option value="ollama">Ollama (Local)</option>
                  <option value="huggingface">Hugging Face</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">
                  API Key
                </label>
                <input
                  type="password"
                  className="input"
                  placeholder="Enter API key"
                  value={newKey.key}
                  onChange={(e) => setNewKey({ ...newKey, key: e.target.value })}
                />
              </div>
              
              <div className="flex gap-4">
                <button
                  onClick={handleAdd}
                  className="btn btn-primary flex-1"
                >
                  Add Key
                </button>
                <button
                  onClick={() => {
                    setShowAddModal(false)
                    setNewKey({ name: '', service: 'openai', key: '' })
                  }}
                  className="btn btn-secondary flex-1"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
