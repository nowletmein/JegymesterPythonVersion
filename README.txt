This project is the backend for Jegymester School project implemented in python


to try out endpoints with swagger (/swagger)
Update-database apply migrations
register a test user
create an Admin role (comment out the @role_required(["Admin"])
@bp.doc(security='ApiKeyAuth') part in app/blueprints/User at the endpoint of role creation (line 43) and at add_role_to_user (line 101))
add a Admin role to test user useing endpoint
login with user
paste users jwt to Authentication in swagger
