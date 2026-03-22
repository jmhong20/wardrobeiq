from datetime import date, datetime
from pydantic import BaseModel, Field


class WearLogCreate(BaseModel):
    item_ids: list[int]          # items being logged (required)
    outfit_id: int | None = None # link to an existing outfit if applicable
    worn_date: date = Field(default_factory=date.today)
    occasion_tag: str | None = None
    weather_context: str | None = None
    notes: str | None = None


class WearLogRead(BaseModel):
    id: int
    user_id: int
    outfit_id: int | None
    worn_date: date
    occasion_tag: str | None
    weather_context: str | None
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
