from datetime import date

from sqlalchemy.orm import Session

from ..models.item import ClothingItem
from ..models.wear_log import WearLog
from ..schemas.wear_log import WearLogCreate


def log_wear(db: Session, user_id: int, payload: WearLogCreate) -> WearLog:
    # Create the wear log record
    log = WearLog(
        user_id=user_id,
        outfit_id=payload.outfit_id,
        worn_date=payload.worn_date,
        occasion_tag=payload.occasion_tag,
        weather_context=payload.weather_context,
        notes=payload.notes,
    )
    db.add(log)

    # Update wear_count and last_worn for each item
    items = (
        db.query(ClothingItem)
        .filter(
            ClothingItem.id.in_(payload.item_ids),
            ClothingItem.user_id == user_id,
        )
        .all()
    )
    for item in items:
        item.wear_count += 1
        if item.last_worn is None or payload.worn_date > item.last_worn:
            item.last_worn = payload.worn_date

    db.commit()
    db.refresh(log)
    return log


def get_wear_history(db: Session, user_id: int, limit: int = 50) -> list[WearLog]:
    return (
        db.query(WearLog)
        .filter(WearLog.user_id == user_id)
        .order_by(WearLog.worn_date.desc())
        .limit(limit)
        .all()
    )
