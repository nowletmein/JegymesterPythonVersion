from app.extensions import db
from sqlalchemy import Column, Integer, ForeignKey

# User <-> Role
user_roles = db.Table(
    "user_roles",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

# User <-> Screening (Cart)
shopping_cart = db.Table(
    "shopping_cart",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("screening_id", Integer, ForeignKey("screenings.id"), primary_key=True),
)