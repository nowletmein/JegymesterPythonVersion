from __future__ import annotations
from datetime import datetime
from sqlalchemy import ForeignKey, String, Boolean, DateTime as SqlDateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .user import User
    from .screening import Screening

class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    screening_id: Mapped[int] = mapped_column(ForeignKey("screenings.id"))
    
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(120))
    purchase_date: Mapped[datetime] = mapped_column(SqlDateTime, default=datetime.utcnow)
    
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    owner: Mapped[Optional["User"]] = relationship(back_populates="tickets")
    screening: Mapped["Screening"] = relationship(back_populates="tickets")