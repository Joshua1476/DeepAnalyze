import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Cloud, Plus, Trash2, ArrowLeft } from 'lucide-react'

export default function Providers() {
  const navigate = useNavigate()
  const [providers, setProviders] = useState([
    { id: 1, name: 'Google Drive', type: 'gdrive', connected: false },
    { id: 2, name: 'Dropbox', type: 'dropbox', connected: false },
    { id: 3, name: 'OneDrive', type: 'onedrive', connected: false },
  ])
  
  const [showAddModal, setShowAddModal] = useState(false)
  const [selectedProvider, setSelectedProvider] = useState(null)
  const [credentials, setCredentials] = useState({})
  
  const handleConnect = (provider) => {
    setSelectedProvider(provider)
    setShowAddModal(true)
  }
  
  const handleSave = () => {
    // TODO: Save credentials to backend
    setProviders(providers.map(p =>
      p.id === selectedProvider.id ? { ...p, connected: true } : p
    ))
    setShowAddModal(false)
    setCredentials({})
  }
  
  const handleDisconnect = (providerId) => {
    setProviders(providers.map(p =>
      p.id === providerId ? { ...p, connected: false } : p
    ))
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
              Cloud Storage Providers
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Connect your cloud storage accounts
            </p>
          </div>
        </div>
      </header>
      
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {providers.map((provider) => (
            <div key={provider.id} className="card">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <Cloud size={32} className="text-primary-600" />
                  <div>
                    <h3 className="text-lg font-semibold">{provider.name}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {provider.connected ? 'Connected' : 'Not connected'}
                    </p>
                  </div>
                </div>
                {provider.connected && (
                  <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                    Active
                  </span>
                )}
              </div>
              
              {provider.connected ? (
                <button
                  onClick={() => handleDisconnect(provider.id)}
                  className="btn btn-secondary w-full flex items-center justify-center gap-2"
                >
                  <Trash2 size={20} />
                  Disconnect
                </button>
              ) : (
                <button
                  onClick={() => handleConnect(provider)}
                  className="btn btn-primary w-full flex items-center justify-center gap-2"
                >
                  <Plus size={20} />
                  Connect
                </button>
              )}
            </div>
          ))}
        </div>
      </main>
      
      {/* Add Provider Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="card max-w-md w-full">
            <h2 className="text-xl font-bold mb-4">
              Connect {selectedProvider?.name}
            </h2>
            
            <div className="space-y-4">
              {selectedProvider?.type === 'gdrive' && (
                <>
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Client ID
                    </label>
                    <input
                      type="text"
                      className="input"
                      placeholder="Enter Google Drive Client ID"
                      onChange={(e) => setCredentials({ ...credentials, client_id: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Client Secret
                    </label>
                    <input
                      type="password"
                      className="input"
                      placeholder="Enter Client Secret"
                      onChange={(e) => setCredentials({ ...credentials, client_secret: e.target.value })}
                    />
                  </div>
                </>
              )}
              
              {selectedProvider?.type === 'dropbox' && (
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Access Token
                  </label>
                  <input
                    type="password"
                    className="input"
                    placeholder="Enter Dropbox Access Token"
                    onChange={(e) => setCredentials({ ...credentials, access_token: e.target.value })}
                  />
                </div>
              )}
              
              <div className="flex gap-4">
                <button
                  onClick={handleSave}
                  className="btn btn-primary flex-1"
                >
                  Save
                </button>
                <button
                  onClick={() => {
                    setShowAddModal(false)
                    setCredentials({})
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
