const CATEGORY_EMOJI = {
  top: '👕', bottom: '👖', outerwear: '🧥',
  shoes: '👟', accessory: '💍', dress: '👗', other: '🧺',
}

function ItemThumb({ item }) {
  return (
    <div className="outfit-thumb">
      {item.image_path
        ? <img src={item.image_path} alt={item.name} />
        : <span>{CATEGORY_EMOJI[item.category] || '👔'}</span>
      }
      <p className="outfit-thumb-label">{item.name}</p>
    </div>
  )
}

export default function OutfitCard({ suggestion, onAccept, onDismiss, accepted }) {
  const { items, score, rationale } = suggestion

  return (
    <div className={`outfit-card ${accepted ? 'outfit-card--accepted' : ''}`}>
      <div className="outfit-thumbs">
        {items.map((item) => <ItemThumb key={item.id} item={item} />)}
      </div>

      <div className="outfit-meta">
        <span className="outfit-score">Score {(score * 100).toFixed(0)}</span>
        <span className="outfit-rationale">{rationale}</span>
      </div>

      {!accepted ? (
        <div className="outfit-actions">
          <button className="btn-primary" onClick={() => onAccept(suggestion)}>
            ✓ Wear this
          </button>
          <button className="btn-ghost" onClick={() => onDismiss(suggestion)}>
            Dismiss
          </button>
        </div>
      ) : (
        <p className="outfit-logged">Logged! ✓</p>
      )}
    </div>
  )
}
