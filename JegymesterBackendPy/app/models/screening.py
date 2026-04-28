from __future__ import annotations
from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


if TYPE_CHECKING:
    from .movie import Movie
    from .room import Room
    from .ticket import Ticket

class Screening(db.Model):
    __tablename__ = "screenings"

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int] = mapped_column(default=0)
    screening_date: Mapped[datetime] = mapped_column(DateTime)
    
    # Foreign Keys - These use the lowercase TABLE names
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    
    movie: Mapped["Movie"] = relationship(back_populates="screenings")
    room: Mapped["Room"] = relationship(back_populates="screenings")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="screening")

    def __repr__(self) -> str:
        return f"Screening(id={self.id}, date={self.screening_date})"