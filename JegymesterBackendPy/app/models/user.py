from __future__ import annotations
from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from .associations import user_roles, shopping_cart

if TYPE_CHECKING:
    from role import Role
    from screening import Screening
    from ticket import Ticket

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    phone: Mapped[str] = mapped_column(String(14))
    password: Mapped[str] = mapped_column(String(255))

    # Relationships
    roles: Mapped[List["Role"]] = relationship(secondary=user_roles, back_populates="users")
    cart_items: Mapped[List["Screening"]] = relationship(secondary=shopping_cart)
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="owner")