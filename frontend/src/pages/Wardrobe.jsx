import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getItems } from '../api/items'
import ItemCard from '../components/ItemCard'

const CATEGORIES = ['all', 'top', 'bottom', 'outerwear', 'shoes', 'accessory', 'dress', 'other']

export default function Wardrobe() {
  const [items, setItems] = useState([])
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    const params = filter !== 'all' ? { category: filter } : {}
    getItems(params)
      .then((res) => setItems(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [filter])

  return (
    <div className="page">
      <div className="page-header">
        <h1>My Wardrobe <span className="item-count">({items.length})</span></h1>
        <Link to="/wardrobe/add" className="btn-primary">+ Add Item</Link>
      </div>

      <div className="filter-bar">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            className={`filter-chip ${filter === cat ? 'active' : ''}`}
            onClick={() => setFilter(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {error && <p className="error-msg">{error}</p>}
      {loading && <p className="muted">Loading…</p>}

      {!loading && items.length === 0 && (
        <div className="empty-state">
          <p>No items yet.</p>
          <Link to="/wardrobe/add" className="btn-primary">Add your first item</Link>
        </div>
      )}

      <div className="item-grid">
        {items.map((item) => (
          <ItemCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  )
}
