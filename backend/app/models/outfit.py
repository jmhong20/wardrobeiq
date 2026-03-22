from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, JSON, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from ..core.database import Base


class OutfitSource(str, enum.Enum):
    manual = "manual"
    ai_suggested = "ai_suggested"
    rule_engine = "rule_engine"


class Outfit(Base):
    __tablename__ = "outfits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    item_ids: Mapped[list] = mapped_column(JSON, default=list)  # list of clothing_item IDs
    source: Mapped[OutfitSource] = mapped_column(Enum(OutfitSource), default=OutfitSource.manual)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 1-5
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    owner: Mapped["User"] = relationship("User", back_populates="outfits")
    wear_logs: Mapped[list["WearLog"]] = relationship("WearLog", back_populates="outfit")
