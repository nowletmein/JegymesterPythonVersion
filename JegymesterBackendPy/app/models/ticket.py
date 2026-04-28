from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from user import User
    from screening import Screening

class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # FKs
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    screening_id: Mapped[int] = mapped_column(ForeignKey("screenings.id"))

    # Navigation Objects
    owner: Mapped["User"] = relationship(back_populates="tickets")
    screening: Mapped["Screening"] = relationship(back_populates="tickets")