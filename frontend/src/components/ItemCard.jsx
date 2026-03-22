import { Link } from 'react-router-dom'

const CATEGORY_EMOJI = {
  top: '👕', bottom: '👖', outerwear: '🧥',
  shoes: '👟', accessory: '💍', dress: '👗', other: '🧺',
}

const STARS = [1, 2, 3, 4, 5]

export default function ItemCard({ item }) {
  return (
    <Link to={`/wardrobe/${item.id}`} className="item-card">
      <div className="item-card-img">
        {item.image_path ? (
          <img src={item.image_path} alt={item.name} />
        ) : (
          <span className="item-card-placeholder">
            {CATEGORY_EMOJI[item.category] || '👔'}
          </span>
        )}
      </div>
      <div className="item-card-body">
        <p className="item-card-name">{item.name}</p>
        <p className="item-card-category">{item.category}</p>
        <p className="item-card-stars">
          {STARS.map((s) => (
            <span key={s} style={{ opacity: s <= item.favorability ? 1 : 0.25 }}>★</span>
          ))}
          <span className="item-card-wear"> · {item.wear_count}×</span>
        </p>
      </div>
    </Link>
  )
}
