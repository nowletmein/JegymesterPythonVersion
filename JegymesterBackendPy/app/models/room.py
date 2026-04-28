from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

if TYPE_CHECKING:
    from screening import Screening

class Room(db.Model):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    capacity: Mapped[int] = mapped_column()

    screenings: Mapped[List["Screening"]] = relationship(back_populates="room")