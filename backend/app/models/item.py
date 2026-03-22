from datetime import datetime, date
from sqlalchemy import String, Integer, Boolean, Date, DateTime, ForeignKey, JSON, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from ..core.database import Base


class CategoryEnum(str, enum.Enum):
    top = "top"
    bottom = "bottom"
    outerwear = "outerwear"
    shoes = "shoes"
    accessory = "accessory"
    dress = "dress"
    other = "other"


class ClothingItem(Base):
    __tablename__ = "clothing_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    category: Mapped[CategoryEnum] = mapped_column(Enum(CategoryEnum), nullable=False, index=True)
    style_tags: Mapped[list] = mapped_column(JSON, default=list)
    color_tags: Mapped[list] = mapped_column(JSON, default=list)
    season_tags: Mapped[list] = mapped_column(JSON, default=list)
    favorability: Mapped[int] = mapped_column(Integer, default=3)  # 1-5
    wear_count: Mapped[int] = mapped_column(Integer, default=0, index=True)
    last_worn: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    owner: Mapped["User"] = relationship("User", back_populates="items")
