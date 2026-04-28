from app.extensions import db
from flask import current_app
from app.blueprints.User.schemas import PayloadSchema, UserResponseSchema, RoleSchema
from app.models.user import User
from app.models.role import Role
from app.models.screening import Screening
from datetime import datetime, timedelta
from sqlalchemy import select
from authlib.jose import jwt
from sqlalchemy.orm import selectinload
from app.utils.date_utils import ensure_datetime

class UserService:

    @staticmethod
    def get(user_id):
        stmt = select(User).where(User.id == user_id).options(
            selectinload(User.roles),
            selectinload(User.shopping_cart),
            selectinload(User.tickets)
        )
        user = db.session.execute(stmt).scalar_one_or_none()
        
        if not user:
            return False, f"User not found with Id: {user_id}"

        cart_data = []
        for s in user.shopping_cart:
            cart_data.append({
                "id": s.id,
                "movie_id": s.movie_id,
                "room_id": s.room_id,
                "price": s.price,
                "screening_date": ensure_datetime(s.screening_date)
            })

        ticket_data = []
        for t in user.tickets:
            ticket_data.append({
                "id": t.id,
                "screening_id": t.screening_id,
                "phone": t.phone,
                "email": t.email,
                "purchase_date": ensure_datetime(t.purchase_date),
                "is_cancelled": t.is_cancelled,
                "is_verified": t.is_verified
            })

        user_dict = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "roles": RoleSchema().dump(user.roles, many=True),
            "shopping_cart": cart_data,
            "tickets": ticket_data
        }
            
        return True, user_dict

    @staticmethod
    def register(request):
        try:
            if db.session.execute(select(User).filter_by(email=request["email"])).scalar_one_or_none():
                return False, "User with this email address already exists"

            user = User(
                name=request.get("name"),
                email=request.get("email"),
                phone=request.get("phone")
            )
            user.set_password(request.get("password"))

            user_role = db.session.execute(select(Role).filter_by(name="User")).scalar_one_or_none()
            if not user_role:
                user_role = Role(name="User")
                db.session.add(user_role)
            
            user.roles.append(user_role)
            db.session.add(user)
            db.session.commit()
            
            # Re-fetch with relationships to ensure the dump works perfectly
            return UserService.get(user.id)
        except Exception:
            db.session.rollback()
            return False, "Error during registration"

    @staticmethod
    def edit(user_id, request):
        try:
            user = db.session.get(User, user_id)
            if not user:
                return False, f"User not found with Id: {user_id}"

            for key, value in request.items():
                # 1. Skip if it's a standard string placeholder or null
                if value is None or value == "" or value == "string":
                    continue

                # 2. Skip if it's 0 (unless it's a boolean False, which we might want to save)
                # This handles the "int default is 0" issue in Swagger/JSON
                if value == 0 and not isinstance(value, bool):
                    continue

                # 3. Only update if the User model actually has this field
                if hasattr(user, key):
                    if key == "password":
                        user.set_password(value)
                    else:
                        setattr(user, key, value)

            db.session.commit()
            return True, user.id
        except Exception:
            db.session.rollback()
            return False, "Error updating user"


    @staticmethod
    def login(email, password):
        try:
            user = db.session.execute(select(User).filter_by(email=email)).scalar_one_or_none()
            if not user or not user.check_password(password):
                return False, "Bad email or password"
            
            user_data = UserResponseSchema().dump(user)
            user_data["token"] = UserService.token_generate(user)
            return True, user_data
        except Exception:
            return False, "Login failed"

    @staticmethod
    def get_roles():
        roles = db.session.query(Role).all()
        return True, RoleSchema().dump(roles, many=True)

    @staticmethod
    def create_role(request):
        try:
            role = Role(name=request.get("name"))
            db.session.add(role)
            db.session.commit()
            return True, role.id
        except Exception:
            db.session.rollback()
            return False, "Error creating role"

    @staticmethod
    def add_role_to_user(role_id, user_id):
        user = db.session.get(User, user_id)
        role = db.session.get(Role, role_id)
        if not user or not role:
            return False, f"User or Role does not exist with this Id: {user_id}"
        
        if role not in user.roles:
            user.roles.append(role)
            db.session.commit()
        return True, 0

    @staticmethod
    def add_to_cart(user_id, screening_id):
        user = db.session.get(User, user_id)
        screening = db.session.get(Screening, screening_id)
        if not user or not screening:
            return False, "Screening or User not found"
        
        user.shopping_cart.append(screening)
        db.session.commit()
        return True, screening.id

    @staticmethod
    def remove_from_cart(user_id, screening_id):
        user = db.session.get(User, user_id)
        if not user:
            return False, f"User does not exist with this id: {user_id}"
        
        screening = next((s for s in user.shopping_cart if s.id == screening_id), None)
        if not screening:
            return False, f"Screening with this Id doesn't exist in this user's cart Id: {screening_id}"
        
        user.shopping_cart.remove(screening)
        db.session.commit()
        return True, screening.id

    @staticmethod
    def token_generate(user: User):
        payload = PayloadSchema()
        payload.exp = int((datetime.now() + timedelta(minutes=30)).timestamp())
        payload.user_id = user.id
        payload.roles = RoleSchema().dump(obj=user.roles, many=True)
        return jwt.encode({'alg': 'HS256'}, PayloadSchema().dump(payload), current_app.config['SECRET_KEY']).decode()