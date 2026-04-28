from apiflask import APIBlueprint

bp = APIBlueprint('movie', __name__, tag="movie")
bp.security = [{'ApiKeyAuth': []}]
from app.blueprints.Movie import routes