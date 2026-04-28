from apiflask import Schema
from apiflask.fields import String, Integer, DateTime, Boolean

class TicketResponseSchema(Schema):
    id = Integer()
    screening_id = Integer()
    user_id = Integer(allow_none=True)
    phone = String()
    email = String()
    purchase_date = DateTime()
    is_cancelled = Boolean()
    is_verified = Boolean()

class TicketCreateSchema(Schema):
    screening_id = Integer(required=True)
    user_id = Integer(allow_none=True)
    phone = String(required=True)
    email = String(required=True)