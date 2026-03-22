import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Register from './pages/Register'
import Wardrobe from './pages/Wardrobe'
import AddItem from './pages/AddItem'
import ItemDetail from './pages/ItemDetail'
import Suggestions from './pages/Suggestions'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <AuthProvider>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/wardrobe" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/wardrobe" element={
          <ProtectedRoute><Wardrobe /></ProtectedRoute>
        } />
        <Route path="/wardrobe/add" element={
          <ProtectedRoute><AddItem /></ProtectedRoute>
        } />
        <Route path="/wardrobe/:id" element={
          <ProtectedRoute><ItemDetail /></ProtectedRoute>
        } />
        <Route path="/suggestions" element={
          <ProtectedRoute><Suggestions /></ProtectedRoute>
        } />
        <Route path="/dashboard" element={
          <ProtectedRoute><Dashboard /></ProtectedRoute>
        } />
      </Routes>
    </AuthProvider>
  )
}

export default App
