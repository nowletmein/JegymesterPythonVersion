from __future__ import annotations 
from typing import List, Optional, TYPE_CHECKING 
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

# 3. This block only runs for your IDE/Type Checker
if TYPE_CHECKING:
    from .screening import Screening 

class Movie(db.Model):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    # ... other columns ...

    # Now the squiggle for "Screening" will disappear!
    screenings: Mapped[List["Screening"]] = relationship(back_populates="movie")