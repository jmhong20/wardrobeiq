import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createItem } from '../api/items'

const CATEGORIES = ['top', 'bottom', 'outerwear', 'shoes', 'accessory', 'dress', 'other']
const SEASONS = ['spring', 'summer', 'fall', 'winter']

export default function AddItem() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    name: '',
    category: 'top',
    favorability: 3,
    style_tags: '',
    color_tags: '',
    season_tags: [],
  })
  const [imageFile, setImageFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleImage = (e) => {
    const file = e.target.files[0]
    if (!file) return
    setImageFile(file)
    setPreview(URL.createObjectURL(file))
  }

  const toggleSeason = (season) => {
    setForm((f) => ({
      ...f,
      season_tags: f.season_tags.includes(season)
        ? f.season_tags.filter((s) => s !== season)
        : [...f.season_tags, season],
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    const fd = new FormData()
    fd.append('name', form.name)
    fd.append('category', form.category)
    fd.append('favorability', form.favorability)
    fd.append('style_tags', JSON.stringify(
      form.style_tags.split(',').map((s) => s.trim()).filter(Boolean)
    ))
    fd.append('color_tags', JSON.stringify(
      form.color_tags.split(',').map((s) => s.trim()).filter(Boolean)
    ))
    fd.append('season_tags', JSON.stringify(form.season_tags))
    if (imageFile) fd.append('image', imageFile)

    try {
      const { data } = await createItem(fd)
      navigate(`/wardrobe/${data.id}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add item.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <h1>Add Item</h1>
      <form className="item-form" onSubmit={handleSubmit}>
        {error && <p className="error-msg">{error}</p>}

        {/* Image upload */}
        <div className="image-upload-area" onClick={() => document.getElementById('img-input').click()}>
          {preview
            ? <img src={preview} alt="preview" />
            : <span>Click to upload photo</span>
          }
          <input id="img-input" type="file" accept="image/*" hidden onChange={handleImage} />
        </div>

        <label>
          Name *
          <input
            type="text"
            required
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
        </label>

        <label>
          Category *
          <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
            {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
        </label>

        <label>
          Favorability
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
        </label>

        <label>
          Style tags <span className="hint">(comma-separated, e.g. casual, streetwear)</span>
          <input
            type="text"
            value={form.style_tags}
            onChange={(e) => setForm({ ...form, style_tags: e.target.value })}
          />
        </label>

        <label>
          Color tags <span className="hint">(e.g. navy, white)</span>
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
          <button type="button" className="btn-ghost" onClick={() => navigate('/wardrobe')}>
            Cancel
          </button>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Saving…' : 'Save Item'}
          </button>
        </div>
      </form>
    </div>
  )
}
