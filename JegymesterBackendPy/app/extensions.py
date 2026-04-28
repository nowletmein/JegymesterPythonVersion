from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

#Database config
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)


#Auth
from apiflask import HTTPTokenAuth
auth = HTTPTokenAuth()
