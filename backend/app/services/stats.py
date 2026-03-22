from collections import Counter
from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.item import ClothingItem
from ..models.wear_log import WearLog


def get_summary(db: Session, user_id: int) -> dict:
    items = (
        db.query(ClothingItem)
        .filter(ClothingItem.user_id == user_id, ClothingItem.active == True)
        .all()
    )
    total = len(items)
    worn = sum(1 for i in items if i.wear_count > 0)
    total_wears = sum(i.wear_count for i in items)
    avg_favorability = round(sum(i.favorability for i in items) / total, 1) if total else 0

    most_worn = max(items, key=lambda i: i.wear_count, default=None)
    least_loved = [i for i in items if i.wear_count == 0]

    return {
        "total_items": total,
        "total_worn": worn,
        "total_never_worn": total - worn,
        "total_wears": total_wears,
        "avg_favorability": avg_favorability,
        "most_worn_item": {
            "id": most_worn.id,
            "name": most_worn.name,
            "wear_count": most_worn.wear_count,
            "image_path": most_worn.image_path,
        } if most_worn and most_worn.wear_count > 0 else None,
        "never_worn_count": len(least_loved),
    }


def get_by_category(db: Session, user_id: int) -> list[dict]:
    rows = (
        db.query(ClothingItem.category, func.count(ClothingItem.id).label("count"))
        .filter(ClothingItem.user_id == user_id, ClothingItem.active == True)
        .group_by(ClothingItem.category)
        .all()
    )
    return [{"category": r.category.value, "count": r.count} for r in rows]


def get_style_breakdown(db: Session, user_id: int) -> list[dict]:
    items = (
        db.query(ClothingItem)
        .filter(ClothingItem.user_id == user_id, ClothingItem.active == True)
        .all()
    )
    counter: Counter = Counter()
    for item in items:
        for tag in (item.style_tags or []):
            counter[tag] += 1

    return [{"style": k, "count": v} for k, v in counter.most_common(10)]


def get_never_worn(db: Session, user_id: int) -> list[dict]:
    items = (
        db.query(ClothingItem)
        .filter(
            ClothingItem.user_id == user_id,
            ClothingItem.active == True,
            ClothingItem.wear_count == 0,
        )
        .order_by(ClothingItem.created_at.asc())
        .all()
    )
    return [
        {"id": i.id, "name": i.name, "category": i.category.value, "image_path": i.image_path}
        for i in items
    ]


def get_most_worn(db: Session, user_id: int, limit: int = 5) -> list[dict]:
    items = (
        db.query(ClothingItem)
        .filter(
            ClothingItem.user_id == user_id,
            ClothingItem.active == True,
            ClothingItem.wear_count > 0,
        )
        .order_by(ClothingItem.wear_count.desc())
        .limit(limit)
        .all()
    )
    return [
        {"id": i.id, "name": i.name, "category": i.category.value,
         "wear_count": i.wear_count, "image_path": i.image_path}
        for i in items
    ]


_EXPECTED_MINIMUMS = {
    "top": 3, "bottom": 3, "shoes": 2, "outerwear": 1,
}

def get_wardrobe_gaps(db: Session, user_id: int) -> list[dict]:
    counts = {r["category"]: r["count"] for r in get_by_category(db, user_id)}
    gaps = []
    for category, minimum in _EXPECTED_MINIMUMS.items():
        have = counts.get(category, 0)
        if have < minimum:
            gaps.append({
                "category": category,
                "have": have,
                "recommended": minimum,
                "message": f"You have {have} {category}(s) — consider adding {minimum - have} more.",
            })

    # Imbalance check: tops vs bottoms
    tops = counts.get("top", 0)
    bottoms = counts.get("bottom", 0)
    if tops > 0 and bottoms > 0 and max(tops, bottoms) / max(min(tops, bottoms), 1) >= 3:
        more = "tops" if tops > bottoms else "bottoms"
        less = "bottoms" if tops > bottoms else "tops"
        gaps.append({
            "category": less,
            "have": min(tops, bottoms),
            "recommended": max(tops, bottoms),
            "message": f"You have {tops} top(s) but only {bottoms} bottom(s) — wardrobe feels unbalanced.",
        })

    return gaps


def get_wear_calendar(db: Session, user_id: int, days: int = 90) -> list[dict]:
    since = date.today() - timedelta(days=days)
    rows = (
        db.query(WearLog.worn_date, func.count(WearLog.id).label("count"))
        .filter(WearLog.user_id == user_id, WearLog.worn_date >= since)
        .group_by(WearLog.worn_date)
        .all()
    )
    return [{"date": str(r.worn_date), "count": r.count} for r in rows]


def export_wardrobe(db: Session, user_id: int) -> list[dict]:
    items = (
        db.query(ClothingItem)
        .filter(ClothingItem.user_id == user_id, ClothingItem.active == True)
        .order_by(ClothingItem.category)
        .all()
    )
    return [
        {
            "id": i.id,
            "name": i.name,
            "category": i.category.value,
            "style_tags": i.style_tags,
            "color_tags": i.color_tags,
            "season_tags": i.season_tags,
            "favorability": i.favorability,
            "wear_count": i.wear_count,
            "last_worn": str(i.last_worn) if i.last_worn else None,
            "created_at": str(i.created_at),
        }
        for i in items
    ]
