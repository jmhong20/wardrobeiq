import { useEffect, useState } from 'react'
import { getSuggestions } from '../api/recommendations'
import { createOutfit } from '../api/outfits'
import { logWear } from '../api/wearLogs'
import OutfitCard from '../components/OutfitCard'

const SEASONS = ['spring', 'summer', 'fall', 'winter']

export default function Suggestions() {
  const [suggestions, setSuggestions] = useState([])
  const [dismissed, setDismissed] = useState(new Set())
  const [accepted, setAccepted] = useState(new Set())
  const [season, setSeason] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [visibleCount, setVisibleCount] = useState(10)

  const fetchSuggestions = (s = season) => {
    setLoading(true)
    setError(null)
    setDismissed(new Set())
    setAccepted(new Set())
    setVisibleCount(10)
    getSuggestions(50, s)
      .then((res) => setSuggestions(res.data))
      .catch((err) => setError(err.response?.data?.detail || err.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchSuggestions() }, [])

  const handleAccept = async (suggestion) => {
    try {
      // Save outfit then log the wear
      const { data: outfit } = await createOutfit({
        item_ids: suggestion.item_ids,
        source: 'rule_engine',
      })
      await logWear({
        item_ids: suggestion.item_ids,
        outfit_id: outfit.id,
      })
      setAccepted((prev) => new Set([...prev, suggestion.item_ids.join(',')]))
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to log wear.')
    }
  }

  const handleDismiss = (suggestion) => {
    setDismissed((prev) => new Set([...prev, suggestion.item_ids.join(',')]))
  }

  const visible = suggestions.filter(
    (s) => !dismissed.has(s.item_ids.join(','))
  )
  const displayed = visible.slice(0, visibleCount)
  const hasMore = visible.length > visibleCount

  return (
    <div className="page">
      <div className="page-header">
        <h1>Outfit Suggestions</h1>
        <button className="btn-ghost" onClick={() => fetchSuggestions()}>↺ Refresh</button>
      </div>

      {/* Season filter */}
      <div className="filter-bar" style={{ marginBottom: '1.5rem' }}>
        <button
          className={`filter-chip ${!season ? 'active' : ''}`}
          onClick={() => { setSeason(null); fetchSuggestions(null) }}
        >auto</button>
        {SEASONS.map((s) => (
          <button
            key={s}
            className={`filter-chip ${season === s ? 'active' : ''}`}
            onClick={() => { setSeason(s); fetchSuggestions(s) }}
          >{s}</button>
        ))}
      </div>

      {error && <p className="error-msg">{error}</p>}
      {loading && <p className="muted">Finding outfits for you…</p>}

      {!loading && visible.length === 0 && !error && (
        <div className="empty-state">
          <p>No suggestions yet — add more items to your wardrobe first.</p>
          <p className="muted" style={{ fontSize: '0.85rem' }}>
            The rule engine needs at least one top and one bottom.
          </p>
        </div>
      )}

      <div className="suggestions-grid">
        {displayed.map((s) => {
          const key = s.item_ids.join(',')
          return (
            <OutfitCard
              key={key}
              suggestion={s}
              accepted={accepted.has(key)}
              onAccept={handleAccept}
              onDismiss={handleDismiss}
            />
          )
        })}
      </div>

      {hasMore && (
        <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
          <button
            className="btn-ghost"
            onClick={() => setVisibleCount((c) => c + 10)}
          >
            Show more ({visible.length - visibleCount} remaining)
          </button>
        </div>
      )}
    </div>
  )
}
