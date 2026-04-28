from app.blueprints.Screening import bp
from app.blueprints.Screening.service import ScreeningService
from app.blueprints.Screening.schemas import ScreeningResponseSchema, ScreeningCreateSchema, WeeklyScheduleSchema
from app.blueprints import role_required
from app.extensions import auth

@bp.get('/get-weekly')
@bp.output(WeeklyScheduleSchema(many=True))
def get_weekly():
    _, screenings = ScreeningService.get_weekly()
    return screenings

@bp.get('/<int:id>')
@bp.output(ScreeningResponseSchema)
def get(id):
    success, result = ScreeningService.get_by_id(id)
    if not success:
        return {"message": result}, 404
    return result

@bp.post('/')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
@bp.input(ScreeningCreateSchema)
def create(json_data):
    success, result = ScreeningService.create(json_data)
    if not success:
        return {"message": result}, 400
    return {"id": result}, 201

@bp.delete('/<int:id>')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
def delete(id):
    success, result = ScreeningService.delete(id)
    if not success:
        return {"message": result}, 404
    return "", 204

@bp.put('/<int:id>')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
@bp.input(ScreeningCreateSchema)
def edit(id, json_data):
    success, result = ScreeningService.edit(id, json_data)
    if not success:
        return {"message": result}, 404
    return result

@bp.post('/test-data')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
def add_test_data():
    success, result = ScreeningService.add_test_data()
    if not success:
        return {"message": result}, 500
    return {"message": result}, 201