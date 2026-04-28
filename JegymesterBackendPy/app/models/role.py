from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from .associations import user_roles


if TYPE_CHECKING:
    from .user import User 


class Role(db.Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    
    
    users: Mapped[List["User"]] = relationship(secondary=user_roles, back_populates="roles")