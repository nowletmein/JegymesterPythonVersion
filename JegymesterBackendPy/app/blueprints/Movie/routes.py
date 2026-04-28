from app.blueprints.Movie import bp
from app.blueprints.Movie.service import MovieService
from app.blueprints.Movie.schemas import MovieResponseSchema, MovieCreateSchema
from app.blueprints import role_required
from app.extensions import auth

@bp.get('/')
@bp.output(MovieResponseSchema(many=True))
def get_all():
    _, movies = MovieService.get_all()
    return movies

@bp.get('/<int:movie_id>')
@bp.output(MovieResponseSchema)
def get(movie_id):
    success, result = MovieService.get_by_id(movie_id)
    if not success:
        return {"message": result}, 404
    return result

@bp.post('/')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
@bp.input(MovieCreateSchema)
def create(json_data):
    success, result = MovieService.create(json_data)
    if not success:
        return {"message": result}, 400
    return {"id": result}, 201

@bp.delete('/<int:movie_id>')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
def delete(movie_id):
    success, result = MovieService.delete(movie_id)
    if not success:
        return {"message": result}, 404
    return "", 204

@bp.put('/<int:movie_id>')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
@bp.input(MovieCreateSchema)
def edit(json_data, movie_id):
    success, result = MovieService.edit(movie_id, json_data)
    if not success:
        return {"message": result}, 404
    return result

@bp.post('/test-data')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
def add_test_data():
    success, result = MovieService.add_test_data()
    if not success:
        return {"message": result}, 500
    return {"message": result}, 201