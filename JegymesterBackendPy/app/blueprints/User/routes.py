from app.extensions import auth
from app.blueprints import role_required
from . import bp
from .schemas import UserResponseSchema, UserRequestSchema, UserLoginSchema, RoleSchema
from .service import UserService
from apiflask import HTTPError

@bp.route('/')
def index():
    return 'This is The User Blueprint'