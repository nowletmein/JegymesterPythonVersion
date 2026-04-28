from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

if TYPE_CHECKING:
    from .screening import Screening

class Movie(db.Model):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    picture_path: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    director: Mapped[str] = mapped_column(String(100))
    rating: Mapped[str] = mapped_column(String(10), nullable=True)
    pg: Mapped[str] = mapped_column(String(10))
    length: Mapped[int] = mapped_column(Integer)

    screenings: Mapped[List["Screening"]] = relationship(back_populates="movie")