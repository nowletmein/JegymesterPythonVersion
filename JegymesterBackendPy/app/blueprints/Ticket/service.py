from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.extensions import db
from app.models.ticket import Ticket
from app.models.screening import Screening

class TicketService:

    @staticmethod
    def _ensure_datetime(value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except Exception:
                return value
        return value

    @staticmethod
    def get_all():
        stmt = select(Ticket).options(selectinload(Ticket.screening))
        tickets = db.session.execute(stmt).scalars().all()
        
        for t in tickets:
            if t.screening:
                t.screening.screening_date = TicketService._ensure_datetime(t.screening.screening_date)
        
        return True, tickets

    @staticmethod
    def get_by_id(id):
        stmt = select(Ticket).filter_by(id=id).options(selectinload(Ticket.screening))
        ticket = db.session.execute(stmt).scalar_one_or_none()

        if not ticket:
            return False, "Ticket Not Found"

        if ticket.screening:
            ticket.screening.screening_date = TicketService._ensure_datetime(ticket.screening.screening_date)

        return True, ticket

    @staticmethod
    def create(json_data):
        try:
            ticket = Ticket(**json_data)
            db.session.add(ticket)
            db.session.commit()
            return True, ticket.id
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    #edit is not implemented in endpoint yet
    @staticmethod
    def edit(id, json_data):
        try:
            ticket = db.session.get(Ticket, id)
            if not ticket:
                return False, "Ticket not found"

            for key, value in json_data.items():
                if value is not None and value != "" and value != 0:
                    if hasattr(ticket, key):
                        setattr(ticket, key, value)

            db.session.commit()
            return TicketService.get_by_id(id)
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete(id):
        try:
            ticket = db.session.get(Ticket, id)
            if not ticket:
                return False, "Ticket not found"
            
            db.session.delete(ticket)
            db.session.commit()
            return True, 0
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    @staticmethod
    def verify(id):
        stmt = select(Ticket).filter_by(id=id).options(selectinload(Ticket.screening))
        ticket = db.session.execute(stmt).scalar_one_or_none()
        
        if not ticket:
            return False, "Ticket not found"
            
        if not ticket.screening:
            return False, "No screening associated with this ticket"
            
        dt = TicketService._ensure_datetime(ticket.screening.screening_date)
        
        if isinstance(dt, datetime):
            if dt < datetime.now():
                return False, "This ticket is for a past screening"
                
        return True, "Ticket is valid"
    @staticmethod
    def cancel(id):
        try:
            stmt = select(Ticket).filter_by(id=id).options(selectinload(Ticket.screening))
            ticket = db.session.execute(stmt).scalar_one_or_none()

            if not ticket:
                return False, "Ticket not found"

            if ticket.screening:
                dt = TicketService._ensure_datetime(ticket.screening.screening_date)
                if isinstance(dt, datetime):
                    if (dt - datetime.now()).total_seconds() < 3600:
                        return False, "Tickets can only be cancelled at least 1 hour before the screening"

            db.session.delete(ticket)
            db.session.commit()
            return True, "Ticket cancelled successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)