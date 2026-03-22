import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [open, setOpen] = useState(false)

  const handleSignOut = () => {
    signOut()
    navigate('/login')
    setOpen(false)
  }

  const close = () => setOpen(false)
  const isActive = (path) => location.pathname === path ? 'nav-link active' : 'nav-link'

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand" onClick={close}>👔 WardrobeIQ</Link>

      {user && (
        <button className="hamburger" onClick={() => setOpen((o) => !o)} aria-label="Menu">
          {open ? '✕' : '☰'}
        </button>
      )}

      <div className={`navbar-links ${open ? 'navbar-links--open' : ''}`}>
        {user ? (
          <>
            <Link className={isActive('/wardrobe')} to="/wardrobe" onClick={close}>Wardrobe</Link>
            <Link className={isActive('/suggestions')} to="/suggestions" onClick={close}>Suggestions</Link>
            <Link className={isActive('/dashboard')} to="/dashboard" onClick={close}>Dashboard</Link>
            <Link className="nav-link nav-link--add" to="/wardrobe/add" onClick={close}>+ Add Item</Link>
            <div className="nav-divider" />
            <span className="navbar-user">{user.username}</span>
            <button className="btn-ghost nav-signout" onClick={handleSignOut}>Sign out</button>
          </>
        ) : (
          <>
            <Link className={isActive('/login')} to="/login" onClick={close}>Login</Link>
            <Link className={isActive('/register')} to="/register" onClick={close}>Register</Link>
          </>
        )}
      </div>
    </nav>
  )
}
