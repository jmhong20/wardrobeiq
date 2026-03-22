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

        # Optional slots: cap to top 5 by score; use [None] if category absent
        outers = by_category.get(CategoryEnum.outerwear.value, [])[:5] or [None]
        shoes = by_category.get(CategoryEnum.shoes.value, [])[:5] or [None]

        # Score all combinations
        scored_pairs = []
        for top, bottom, outer, shoe in itertools.product(tops, bottoms, outers, shoes):
            outfit_items = [i for i in [top, bottom, outer, shoe] if i is not None]
            cohesion = _style_cohesion(outfit_items)
            avg_item_score = sum(scored[i] for i in outfit_items) / len(outfit_items)
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

    def match_item(self, user_id: int, item_id: int) -> list[dict]:
        """Return best-matching items from other categories for a given item."""
        target: ClothingItem | None = (
            self.db.query(ClothingItem)
            .filter(
                ClothingItem.id == item_id,
                ClothingItem.user_id == user_id,
                ClothingItem.active == True,
            )
            .first()
        )
        if target is None:
            return []

        season = _current_season()
        others = (
            self.db.query(ClothingItem)
            .filter(
                ClothingItem.user_id == user_id,
                ClothingItem.active == True,
                ClothingItem.id != item_id,
                ClothingItem.category != target.category,
            )
            .all()
        )

        scored = []
        for item in others:
            score = _score_item(item, season) + _style_cohesion([target, item]) * 0.10
            scored.append((item, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        by_cat: dict[str, list[ClothingItem]] = {}
        for item, _ in scored:
            cat = item.category.value
            if cat not in by_cat:
                by_cat[cat] = []
            if len(by_cat[cat]) < 3:
                by_cat[cat].append(item)

        return [{"category": cat, "items": items} for cat, items in by_cat.items()]
