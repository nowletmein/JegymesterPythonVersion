from apiflask import APIBlueprint
from app.extensions import auth
from flask import current_app
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError

bp = APIBlueprint('main', __name__, tag="default")

@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY'],
        )
        if data["exp"] < int(datetime.now().timestamp()):
            return None
        return data
    except Exception:
        return None

def role_required(roles):
    def wrapper(fn):
        def decorated_function(*args, **kwargs):
            user_roles = [item["name"] for item in auth.current_user.get("roles")]
            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)        
            raise HTTPError(message="Access denied", status_code=403)
        return decorated_function
    return wrapper

# Only User is ready
from .User import bp as bp_user
bp.register_blueprint(bp_user, url_prefix='/user')

# These stay commented until you create the folders/files
# from .movie import bp as bp_movie
# bp.register_blueprint(bp_movie, url_prefix='/movie')

from app.models import *