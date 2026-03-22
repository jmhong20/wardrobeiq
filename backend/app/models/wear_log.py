from datetime import datetime, date
from sqlalchemy import String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core.database import Base


class WearLog(Base):
    __tablename__ = "wear_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    outfit_id: Mapped[int | None] = mapped_column(ForeignKey("outfits.id"), nullable=True, index=True)
    worn_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    weather_context: Mapped[str | None] = mapped_column(String(100), nullable=True)
    occasion_tag: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    owner: Mapped["User"] = relationship("User", back_populates="wear_logs")
    outfit: Mapped["Outfit"] = relationship("Outfit", back_populates="wear_logs")
