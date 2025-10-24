import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Providers from './pages/Providers'
import Keys from './pages/Keys'
import { useAuthStore } from './store/authStore'

function ProtectedRoute({ children }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  return isAuthenticated ? children : <Navigate to="/login" />
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/providers"
          element={
            <ProtectedRoute>
              <Providers />
            </ProtectedRoute>
          }
        />
        <Route
          path="/keys"
          element={
            <ProtectedRoute>
              <Keys />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  )
}

export default App
