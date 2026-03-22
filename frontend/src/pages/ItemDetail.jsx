import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getItem, updateItem, deleteItem, uploadImage } from '../api/items'
import { logWear } from '../api/wearLogs'

const SEASONS = ['spring', 'summer', 'fall', 'winter']

export default function ItemDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [item, setItem] = useState(null)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [logging, setLogging] = useState(false)
  const [loggedToday, setLoggedToday] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    getItem(id)
      .then((res) => {
        setItem(res.data)
        setForm({
          name: res.data.name,
          favorability: res.data.favorability,
          style_tags: (res.data.style_tags || []).join(', '),
          color_tags: (res.data.color_tags || []).join(', '),
          season_tags: res.data.season_tags || [],
        })
      })
      .catch(() => setError('Item not found.'))
      .finally(() => setLoading(false))
  }, [id])

  const handleSave = async () => {
    setSaving(true)
    try {
      const { data } = await updateItem(id, {
        name: form.name,
        favorability: form.favorability,
        style_tags: form.style_tags.split(',').map((s) => s.trim()).filter(Boolean),
        color_tags: form.color_tags.split(',').map((s) => s.trim()).filter(Boolean),
        season_tags: form.season_tags,
      })
      setItem(data)
      setEditing(false)
    } catch (err) {
      setError(err.response?.data?.detail || 'Save failed.')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm(`Remove "${item.name}" from your wardrobe?`)) return
    await deleteItem(id)
    navigate('/wardrobe')
  }

  const handleLogWear = async () => {
    setLogging(true)
    try {
      await logWear({ item_ids: [parseInt(id)] })
      setItem((prev) => ({
        ...prev,
        wear_count: prev.wear_count + 1,
        last_worn: new Date().toISOString().slice(0, 10),
      }))
      setLoggedToday(true)
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to log wear.')
    } finally {
      setLogging(false)
    }
  }

  const handleImageUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const fd = new FormData()
    fd.append('image', file)
    const { data } = await uploadImage(id, fd)
    setItem(data)
  }

  const toggleSeason = (season) => {
    setForm((f) => ({
      ...f,
      season_tags: f.season_tags.includes(season)
        ? f.season_tags.filter((s) => s !== season)
        : [...f.season_tags, season],
    }))
  }

  if (loading) return <div className="page-center">Loading…</div>
  if (error) return <div className="page"><p className="error-msg">{error}</p></div>

  return (
    <div className="page">
      <button className="btn-ghost back-btn" onClick={() => navigate('/wardrobe')}>← Back</button>

      <div className="detail-layout">
        {/* Image */}
        <div className="detail-image-col">
          <div className="detail-image-box">
            {item.image_path
              ? <img src={item.image_path} alt={item.name} />
              : <span className="detail-placeholder">No photo</span>
            }
          </div>
          <label className="btn-ghost upload-btn">
            {item.image_path ? 'Replace photo' : 'Upload photo'}
            <input type="file" accept="image/*" hidden onChange={handleImageUpload} />
          </label>
        </div>

        {/* Info */}
        <div className="detail-info-col">
          {editing ? (
            <>
              <input
                className="detail-name-input"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />

              <div className="star-picker">
                {[1, 2, 3, 4, 5].map((n) => (
                  <button
                    key={n}
                    type="button"
                    className={`star ${n <= form.favorability ? 'active' : ''}`}
                    onClick={() => setForm({ ...form, favorability: n })}
                  >★</button>
                ))}
              </div>

              <label>
                Style tags
                <input
                  type="text"
                  value={form.style_tags}
                  onChange={(e) => setForm({ ...form, style_tags: e.target.value })}
                />
              </label>
              <label>
                Color tags
                <input
                  type="text"
                  value={form.color_tags}
                  onChange={(e) => setForm({ ...form, color_tags: e.target.value })}
                />
              </label>

              <div className="field-group">
                <span className="field-label">Season</span>
                <div className="chip-group">
                  {SEASONS.map((s) => (
                    <button
                      key={s}
                      type="button"
                      className={`filter-chip ${form.season_tags.includes(s) ? 'active' : ''}`}
                      onClick={() => toggleSeason(s)}
                    >{s}</button>
                  ))}
                </div>
              </div>

              <div className="form-actions">
                <button className="btn-ghost" onClick={() => setEditing(false)}>Cancel</button>
                <button className="btn-primary" onClick={handleSave} disabled={saving}>
                  {saving ? 'Saving…' : 'Save'}
                </button>
              </div>
            </>
          ) : (
            <>
              <h1 className="detail-name">{item.name}</h1>
              <p className="detail-meta">{item.category} · worn {item.wear_count}×</p>
              {item.last_worn && <p className="detail-meta muted">Last worn: {item.last_worn}</p>}

              <div className="detail-stars">
                {[1, 2, 3, 4, 5].map((n) => (
                  <span key={n} style={{ opacity: n <= item.favorability ? 1 : 0.25 }}>★</span>
                ))}
              </div>

              {item.style_tags?.length > 0 && (
                <div className="tag-group">
                  {item.style_tags.map((t) => <span key={t} className="tag">{t}</span>)}
                </div>
              )}
              {item.color_tags?.length > 0 && (
                <div className="tag-group">
                  {item.color_tags.map((t) => <span key={t} className="tag tag-color">{t}</span>)}
                </div>
              )}
              {item.season_tags?.length > 0 && (
                <div className="tag-group">
                  {item.season_tags.map((t) => <span key={t} className="tag tag-season">{t}</span>)}
                </div>
              )}

              <div className="form-actions" style={{ marginTop: '1.5rem' }}>
                <button
                  className="btn-primary"
                  onClick={handleLogWear}
                  disabled={logging || loggedToday}
                >
                  {loggedToday ? '✓ Worn today' : logging ? 'Logging…' : '👕 Log a Wear'}
                </button>
                <button className="btn-ghost" onClick={() => setEditing(true)}>Edit</button>
                <button className="btn-danger" onClick={handleDelete}>Remove</button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
