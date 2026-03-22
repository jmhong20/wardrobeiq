"""v3 AI Engine — placeholder for Phase 5 (CLIP / LLM-based recommendations).

Swap this in by updating the engine dependency in routers/recommendations.py.
"""

from .base import RecommendationEngine


class AIEngine(RecommendationEngine):
    def suggest(self, user_id: int, context: dict) -> list[dict]:
        raise NotImplementedError("AI engine is planned for Phase 5.")
