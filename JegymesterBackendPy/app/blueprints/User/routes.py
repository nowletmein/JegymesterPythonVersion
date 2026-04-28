from app.extensions import auth
from app.blueprints import role_required
from app.blueprints.User import bp
from app.blueprints.User.schemas import (
    UserResponseSchema, 
    UserRequestSchema, 
    UserLoginSchema, 
    RoleSchema, 
    UserEditSchema, 
    RoleCreateSchema
)
from app.blueprints.User.service import UserService
from apiflask import HTTPError

@bp.post('/login')
@bp.input(UserLoginSchema)
@bp.output(UserResponseSchema)
def login(json_data):
    success, response = UserService.login(json_data.get('email'), json_data.get('password'))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=401)

@bp.post('/register')
@bp.input(UserRequestSchema)
@bp.output(UserResponseSchema)
def register(json_data):
    success, response = UserService.register(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/roles')
@bp.output(RoleSchema(many=True))
def get_roles():
    success, response = UserService.get_roles()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.put('/roles')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
@bp.input(RoleCreateSchema)
def create_role(json_data):
    success, response = UserService.create_role(json_data)
    if success:
        return {"id": response, "message": "Role created successfully"}, 201
    raise HTTPError(message=response, status_code=400)

@bp.get('/<int:Id>')
@bp.output(UserResponseSchema)
def get_user(Id):
    success, response = UserService.get(Id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=404)

@bp.patch('/<int:Id>')
@auth.login_required
@bp.doc(security='ApiKeyAuth')
@bp.input(UserEditSchema)
def edit_user(Id, json_data):
    success, response = UserService.edit(Id, json_data)
    if success:
        return {"id": response, "message": "User updated successfully"}, 200
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:Id>')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
def delete_user(Id):
    success, response = UserService.delete(Id)
    if success:
        return {"id": response, "message": "User deleted successfully"}, 200
    raise HTTPError(message=response, status_code=400)

@bp.post('/<int:userId>/cart/<int:screeningId>')
@auth.login_required
@bp.doc(security='ApiKeyAuth')
def add_to_cart(userId, screeningId):
    success, response = UserService.add_to_cart(userId, screeningId)
    if success:
        return {"id": response, "message": "Item added to cart"}, 200
    raise HTTPError(message=response, status_code=400)

@bp.delete('/<int:userId>/cart/<int:screeningId>')
@auth.login_required
@bp.doc(security='ApiKeyAuth')
def remove_from_cart(userId, screeningId):
    success, response = UserService.remove_from_cart(userId, screeningId)
    if success:
        return {"id": response, "message": "Item removed from cart"}, 200
    raise HTTPError(message=response, status_code=400)

@bp.put('/<int:userId>/role/<int:roleId>')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
def add_role_to_user(userId, roleId):
    success, response = UserService.add_role_to_user(roleId, userId)
    if success:
        return {"id": response, "message": "Role assigned to user successfully"}, 200
    raise HTTPError(message=response, status_code=400)