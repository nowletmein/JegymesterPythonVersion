from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from flask_migrate import Migrate
#Database config
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)


#Auth
from apiflask import HTTPTokenAuth
auth = HTTPTokenAuth(scheme='Bearer', security_scheme_name='ApiKeyAuth')
migrate = Migrate()
cors = CORS()