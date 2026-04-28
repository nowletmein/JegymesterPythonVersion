from apiflask import APIBlueprint

bp = APIBlueprint('user', __name__, url_prefix='/user', tag='user')

from app.blueprints.User import routes