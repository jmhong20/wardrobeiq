from datetime import datetime, date
from pydantic import BaseModel, Field
from app.models.item import CategoryEnum


class ClothingItemCreate(BaseModel):
    name: str
    category: CategoryEnum
    style_tags: list[str] = []
    color_tags: list[str] = []
    season_tags: list[str] = []
    favorability: int = Field(default=3, ge=1, le=5)


class ClothingItemUpdate(BaseModel):
    name: str | None = None
    category: CategoryEnum | None = None
    style_tags: list[str] | None = None
    color_tags: list[str] | None = None
    season_tags: list[str] | None = None
    favorability: int | None = Field(default=None, ge=1, le=5)
    active: bool | None = None


class ClothingItemRead(BaseModel):
    id: int
    user_id: int
    name: str
    image_path: str | None
    category: CategoryEnum
    style_tags: list[str]
    color_tags: list[str]
    season_tags: list[str]
    favorability: int
    wear_count: int
    last_worn: date | None
    active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
