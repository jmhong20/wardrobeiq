from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..engine.rule_engine import RuleEngine
from ..models.item import ClothingItem
from ..models.user import User
from ..schemas.item import ClothingItemRead

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

CurrentUser = Annotated[User, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_db)]


@router.get("/suggest")
def suggest_outfits(
    current_user: CurrentUser,
    db: DB,
    limit: int = Query(default=5, le=20),
    season: str | None = Query(default=None),
):
    engine = RuleEngine(db)
    suggestions = engine.suggest(current_user.id, {"limit": limit, "season": season})

    # Enrich each suggestion with full item objects
    enriched = []
    for s in suggestions:
        items = (
            db.query(ClothingItem)
            .filter(ClothingItem.id.in_(s["item_ids"]))
            .all()
        )
        enriched.append({
            **s,
            "items": [ClothingItemRead.model_validate(i) for i in items],
        })
    return enriched
