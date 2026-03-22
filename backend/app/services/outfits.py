from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.outfit import Outfit, OutfitSource
from ..schemas.outfit import OutfitCreate, OutfitUpdate


def create_outfit(db: Session, user_id: int, payload: OutfitCreate) -> Outfit:
    outfit = Outfit(
        user_id=user_id,
        name=payload.name,
        item_ids=payload.item_ids,
        source=payload.source,
    )
    db.add(outfit)
    db.commit()
    db.refresh(outfit)
    return outfit


def get_outfits(db: Session, user_id: int, limit: int = 50) -> list[Outfit]:
    return (
        db.query(Outfit)
        .filter(Outfit.user_id == user_id)
        .order_by(Outfit.created_at.desc())
        .limit(limit)
        .all()
    )


def get_outfit(db: Session, user_id: int, outfit_id: int) -> Outfit:
    outfit = db.query(Outfit).filter(
        Outfit.id == outfit_id,
        Outfit.user_id == user_id,
    ).first()
    if not outfit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outfit not found.")
    return outfit


def rate_outfit(db: Session, user_id: int, outfit_id: int, rating: int) -> Outfit:
    outfit = get_outfit(db, user_id, outfit_id)
    outfit.rating = rating
    db.commit()
    db.refresh(outfit)
    return outfit


def update_outfit(db: Session, user_id: int, outfit_id: int, payload: OutfitUpdate) -> Outfit:
    outfit = get_outfit(db, user_id, outfit_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(outfit, field, value)
    db.commit()
    db.refresh(outfit)
    return outfit
