from apiflask import Schema
from apiflask.fields import String, Integer, List, Nested, DateTime

class ScreeningResponseSchema(Schema):
    id = Integer()
    screening_date = DateTime()
    price = Integer()
    room_id = Integer()

class MovieResponseSchema(Schema):
    id = Integer()
    title = String()
    picture_path = String()
    description = String()
    director = String()
    rating = String()
    pg = String()
    length = Integer()
    # This nests the screenings inside the movie object
    screenings = List(Nested(ScreeningResponseSchema))

class MovieCreateSchema(Schema):
    title = String(required=True)
    director = String(required=True)
    pg = String(required=True)
    length = Integer(required=True)
    picture_path = String()
    description = String()
    rating = String()