from apiflask import Schema
from apiflask.fields import String, Integer, DateTime, Nested,List

class ScreeningCreateSchema(Schema):
    screening_date = DateTime(required=True)
    price = Integer(required=True)
    movie_id = Integer(required=True)
    room_id = Integer(required=True)

class ScreeningResponseSchema(Schema):
    id = Integer()
    screening_date = DateTime()
    price = Integer()
    movie_id = Integer()
    room_id = Integer()
class WeeklyScheduleSchema(Schema):
    day = String()
    screenings = List(Nested(ScreeningResponseSchema))
