import { Routes, Route, Navigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import DashboardLayout from './components/common/DashboardLayout'
import Dashboard from './pages/Dashboard'
import Prospects from './pages/Prospects'
import Templates from './pages/Templates'
import Analytics from './pages/Analytics'
import Login from './pages/Login'
import Register from './pages/Register'
import { authService } from './services/auth'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          await authService.getCurrentUser()
          setIsAuthenticated(true)
        } catch (error) {
          localStorage.removeItem('token')
          setIsAuthenticated(false)
        }
      }
      setIsLoading(false)
    }
    checkAuth()
  }, [])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  return (
    <Routes>
      <Route path="/login" element={!isAuthenticated ? <Login onLogin={() => setIsAuthenticated(true)} /> : <Navigate to="/" />} />
      <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/" />} />
      
      {isAuthenticated ? (
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="prospects" element={<Prospects />} />
          <Route path="templates" element={<Templates />} />
          <Route path="analytics" element={<Analytics />} />
        </Route>
      ) : (
        <Route path="*" element={<Navigate to="/login" />} />
      )}
    </Routes>
  )
}

export default App
