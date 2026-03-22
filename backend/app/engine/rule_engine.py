"""v1 Rule Engine — scores items by wear history, favorability, and season.

Scoring formula (from SPEC):
  score(item) =
    (favorability × 0.4)
    + (recency_penalty × 0.35)   # higher if not worn recently
    + (season_match × 0.15)
    + (style_cohesion × 0.10)    # items in outfit share style_tags
"""

import itertools
from datetime import date, timedelta
from sqlalchemy.orm import Session

from .base import RecommendationEngine
from ..models.item import ClothingItem, CategoryEnum


# Categories that form a complete outfit (one per slot)
_OUTFIT_SLOTS = [CategoryEnum.top, CategoryEnum.bottom]
_OPTIONAL_SLOTS = [CategoryEnum.outerwear, CategoryEnum.shoes, CategoryEnum.accessory]

_SEASONS = {"spring", "summer", "fall", "winter"}


def _current_season() -> str:
    month = date.today().month
    if month in (3, 4, 5):
        return "spring"
    elif month in (6, 7, 8):
        return "summer"
    elif month in (9, 10, 11):
        return "fall"
    return "winter"


def _recency_penalty(item: ClothingItem) -> float:
    """Returns 0.0–1.0 where 1.0 means never worn / worn long ago."""
    if item.last_worn is None:
        return 1.0
    days_since = (date.today() - item.last_worn).days
    # Saturates at 60 days
    return min(days_since / 60.0, 1.0)


def _season_match(item: ClothingItem, season: str) -> float:
    tags = [t.lower() for t in (item.season_tags or [])]
    if not tags:
        return 0.5  # neutral — untagged items are always okay
    return 1.0 if season in tags else 0.0


def _score_item(item: ClothingItem, season: str) -> float:
    fav = (item.favorability / 5.0)
    recency = _recency_penalty(item)
    season = _season_match(item, season)
    # style_cohesion is computed at outfit level; default 0.5 here
    return fav * 0.4 + recency * 0.35 + season * 0.15 + 0.5 * 0.10


def _style_cohesion(items: list[ClothingItem]) -> float:
    all_tags = [set(i.style_tags or []) for i in items]
    if not all_tags or len(all_tags) < 2:
        return 0.5
    shared = all_tags[0].intersection(*all_tags[1:])
    union = all_tags[0].union(*all_tags[1:])
    return len(shared) / len(union) if union else 0.5


class RuleEngine(RecommendationEngine):
    def __init__(self, db: Session):
        self.db = db

    def suggest(self, user_id: int, context: dict) -> list[dict]:
        season = context.get("season") or _current_season()
        limit = context.get("limit", 5)

        items: list[ClothingItem] = (
            self.db.query(ClothingItem)
            .filter(ClothingItem.user_id == user_id, ClothingItem.active == True)
            .all()
        )

        if not items:
            return []

        # Score each item
        scored = {item: _score_item(item, season) for item in items}

        # Group by category
        by_category: dict[str, list[ClothingItem]] = {}
        for item in items:
            by_category.setdefault(item.category.value, []).append(item)

        # Sort each category bucket by score
        for cat in by_category:
            by_category[cat].sort(key=lambda i: scored[i], reverse=True)

        tops = by_category.get(CategoryEnum.top.value, [])
        bottoms = by_category.get(CategoryEnum.bottom.value, [])

        if not tops or not bottoms:
            return []

        # Score all (top, bottom) pairs
        scored_pairs = []
        for top, bottom in itertools.product(tops, bottoms):
            outfit_items = [top, bottom]
            cohesion = _style_cohesion(outfit_items)
            avg_item_score = (scored[top] + scored[bottom]) / 2.0
            pair_score = avg_item_score + cohesion * 0.10
            scored_pairs.append((outfit_items, pair_score, cohesion))

        scored_pairs.sort(key=lambda x: x[1], reverse=True)

        suggestions = []
        for outfit_items, pair_score, cohesion in scored_pairs[:limit]:
            suggestions.append(
                {
                    "item_ids": [i.id for i in outfit_items],
                    "score": round(pair_score, 3),
                    "rationale": (
                        f"Selected for season={season}, "
                        f"style cohesion={cohesion:.2f}, "
                        f"avg favorability={sum(i.favorability for i in outfit_items)/len(outfit_items):.1f}"
                    ),
                }
            )

        return suggestions
