from marshmallow import Schema
from apiflask.fields import String, Integer, List, Nested, DateTime, Boolean
from apiflask.validators import Length, Email

# Import the actual classes to avoid name registry conflicts
from app.blueprints.Movie.schemas import ScreeningResponseSchema
# If you have a Ticket schema, import it here too:
# from app.blueprints.Ticket.schemas import TicketResponseSchema

class TicketResponseSchema(Schema):
    id = Integer()
    screening_id = Integer()
    phone = String()
    email = String()
    purchase_date = DateTime()
    is_cancelled = Boolean()
    is_verified = Boolean()

class RoleSchema(Schema):
    id = Integer()
    name = String()

class UserResponseSchema(Schema):
    id = Integer()
    name = String()
    email = String()
    phone = String()
    token = String()
    roles = List(Nested(RoleSchema))
    # Use the class directly instead of a string
    shopping_cart = List(Nested(ScreeningResponseSchema)) 
    tickets = List(Nested(TicketResponseSchema))

class UserRequestSchema(Schema):
    name = String(required=True, validate=Length(min=2, max=80))
    email = String(required=True, validate=Email())
    password = String(required=True, validate=Length(min=6))
    phone = String(validate=Length(max=14))

class PayloadSchema(Schema):
    user_id = Integer()
    roles = List(Nested(RoleSchema))
    exp = Integer()

class UserLoginSchema(Schema):
    email = String(required=True, validate=Email())
    password = String(required=True)

class UserEditSchema(Schema):
    name = String()
    email = String()
    phone = String()
    password = String()

class RoleCreateSchema(Schema):
    name = String(required=True)