from marshmallow import Schema, fields
from apiflask.fields import String, Integer, List, Nested
from apiflask.validators import Length, Email

class RoleSchema(Schema):
    id = Integer()
    name = String()

class UserRequestSchema(Schema):
    name = String(required=True, validate=Length(min=2, max=80))
    email = String(required=True, validate=Email())
    password = String(required=True, validate=Length(min=6))
    phone = String(validate=Length(max=14))

class PayloadSchema(Schema):
    user_id = Integer()
    roles = List(Nested(RoleSchema))
    exp = Integer()

class UserResponseSchema(Schema):
    id = Integer()
    name = String()
    email = String()
    token = String()
    roles = List(Nested(RoleSchema))

class UserLoginSchema(Schema):
    email = String(required=True, validate=Email())
    password = String(required=True)