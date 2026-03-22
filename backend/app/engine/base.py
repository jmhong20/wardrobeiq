from abc import ABC, abstractmethod


class RecommendationEngine(ABC):
    """Strategy pattern base — swap implementations without touching API contract."""

    @abstractmethod
    def suggest(self, user_id: int, context: dict) -> list[dict]:
        """Return a list of suggested outfit item combinations.

        Each dict should contain:
          - item_ids: list[int]
          - score: float
          - rationale: str  (human-readable explanation)
        """
        pass
