from datetime import datetime
from pydantic import BaseModel, Field
from app.models.outfit import OutfitSource


class OutfitCreate(BaseModel):
    name: str | None = None
    item_ids: list[int]
    source: OutfitSource = OutfitSource.manual


class OutfitUpdate(BaseModel):
    name: str | None = None
    rating: int | None = Field(default=None, ge=1, le=5)


class OutfitRead(BaseModel):
    id: int
    user_id: int
    name: str | None
    item_ids: list[int]
    source: OutfitSource
    rating: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
