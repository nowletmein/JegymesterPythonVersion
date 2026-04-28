from apiflask import APIBlueprint
from app.extensions import auth
from flask import current_app
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError
from functools import wraps 

bp = APIBlueprint('main', __name__, tag="default")

@auth.verify_token
def verify_token(token):
    try:
   
        print(f"Using Secret: {current_app.config['SECRET_KEY']}") 
        data = jwt.decode(token.encode('ascii'), current_app.config['SECRET_KEY'])
        return data
    except Exception as e:
        print(f"VERIFY ERROR: {e}") 
        return None

def role_required(roles):
    def decorator(fn):
        @wraps(fn) # Ensures endpoint names don't collide
        def decorated_function(*args, **kwargs):
            # Extract names from roles list (e.g. [{"id":1, "name":"Admin"}])
            user_roles = [item["name"] for item in auth.current_user.get("roles", [])]
            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)        
            raise HTTPError(message="Access denied", status_code=403)
        return decorated_function
    return decorator

# --- Blueprint Registration ---

from .User import bp as bp_user
bp.register_blueprint(bp_user, url_prefix='/user')

from .Movie import bp as bp_movie
bp.register_blueprint(bp_movie, url_prefix='/movie')

from .Screening import bp as bp_screening
bp.register_blueprint(bp_screening, url_prefix='/screening')

from .Ticket import bp as bp_ticket
bp.register_blueprint(bp_ticket, url_prefix='/ticket')

from app.models import *