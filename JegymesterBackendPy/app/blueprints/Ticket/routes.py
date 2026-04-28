from app.blueprints.Ticket import bp
from app.blueprints.Ticket.service import TicketService
from app.blueprints.Ticket.schemas import TicketResponseSchema, TicketCreateSchema
from app.extensions import auth
from app.blueprints import role_required

@bp.post('/create')
@bp.input(TicketCreateSchema)
def create(json_data):
    success, result = TicketService.create(json_data)
    if not success:
        return {"message": result}, 400
    return {"id": result}, 200

@bp.patch('/verify-ticket/<int:ticket_id>')
@auth.login_required
@role_required(["Admin", "Cashier"])
@bp.doc(security='ApiKeyAuth')
def verify(ticket_id):
    success, result = TicketService.verify(ticket_id)
    if not success:
        return {"message": result}, 404
    return result

@bp.get('/get/<int:ticket_id>')
@auth.login_required
@bp.doc(security='ApiKeyAuth')
@bp.output(TicketResponseSchema)
def get(ticket_id):
    success, result = TicketService.get_by_id(ticket_id)
    if not success:
        return {"message": result}, 404
    return result

@bp.delete('/delete/<int:ticket_id>')
@auth.login_required
@role_required(["Admin"])
@bp.doc(security='ApiKeyAuth')
def delete(ticket_id):
    success, result = TicketService.delete(ticket_id)
    if not success:
        return {"message": result}, 404
    return {"message": result}, 200

@bp.patch('/cancel/<int:ticket_id>')
@auth.login_required
@role_required(["Admin","Cashier"])
@bp.doc(security='ApiKeyAuth')
def cancel(ticket_id):
    success, result = TicketService.cancel(ticket_id)
    if not success:
        return {"message": result}, 404
    return result