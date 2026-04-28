from datetime import datetime, timedelta
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.extensions import db
from app.models.screening import Screening
from app.models.movie import Movie
from app.models.room import Room
from app.utils.date_utils import ensure_datetime

class ScreeningService:

    @staticmethod
    def get_by_id(id):
        stmt = (
            select(Screening)
            .filter_by(id=id)
            .options(selectinload(Screening.tickets))
        )

        screening = db.session.execute(stmt).scalar_one_or_none()

        if not screening:
            return False, "Screening Not Found"

        data = {
            "id": screening.id,
            "movie_id": screening.movie_id,
            "room_id": screening.room_id,
            "price": screening.price,
            "screening_date": ensure_datetime(screening.screening_date)
        }

        return True, data

    @staticmethod
    def get_weekly():
        screenings = db.session.execute(select(Screening)).scalars().all()

        if not screenings:
            return True, []

        dates = []
        for s in screenings:
            dt = ensure_datetime(s.screening_date)
            if isinstance(dt, datetime):
                dates.append(dt)

        if not dates:
            return True, []

        min_date = min(dates)

        monday = (min_date - timedelta(days=min_date.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        next_monday = monday + timedelta(days=7)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        grouped = {day: [] for day in days}

        for s in screenings:
            dt = ensure_datetime(s.screening_date)
            if not isinstance(dt, datetime):
                continue

            if not (monday <= dt < next_monday):
                continue

            day_name = dt.strftime('%A')

            grouped[day_name].append({
                "id": s.id,
                "movie_id": s.movie_id,
                "room_id": s.room_id,
                "price": s.price,
                "screening_date": dt
            })

        result = [{"day": day, "screenings": grouped[day]} for day in days]
        return True, result

    @staticmethod
    def create(json_data):
        try:
            s_date = ensure_datetime(json_data.get("screening_date"))

            exists = db.session.query(Screening).filter_by(
                screening_date=s_date,
                movie_id=json_data.get("movie_id"),
                room_id=json_data.get("room_id")
            ).first()

            if exists:
                return False, "Screening already exists with this date, movie, and room"

            screening = Screening(**json_data)
            screening.screening_date = s_date
            
            db.session.add(screening)
            db.session.commit()
            return True, screening.id
        except Exception:
            db.session.rollback()
            return False, "Error creating screening"

    @staticmethod
    def edit(id, json_data):
        try:
            screening = db.session.get(Screening, id)
            if not screening:
                return False, "Screening not found"

            for key, value in json_data.items():
                if value is not None and value != "" and value != 0:
                    if hasattr(screening, key):
                        if key == "screening_date":
                            value = ensure_datetime(value)
                        setattr(screening, key, value)

            db.session.commit()
            
            return ScreeningService.get_by_id(id)
        except Exception:
            db.session.rollback()
            return False, "Error updating screening"

    @staticmethod
    def delete(id):
        try:
            screening = db.session.get(Screening, id)
            if not screening:
                return False, f"Screening Not Found with ID {id}"
            
            db.session.delete(screening)
            db.session.commit()
            return True, "Deleted successfully"
        except Exception:
            db.session.rollback()
            return False, "Error deleting screening"

    @staticmethod
    def add_test_data():
        try:
            db.session.query(Screening).delete()

            movies = db.session.query(Movie).all()
            if not movies:
                return False, "No movies found"

            rooms = db.session.query(Room).all()
            if len(rooms) < 5:
                for i in range(1, 6):
                    db.session.add(Room(name=f"Hall {i}", capacity=100, available=True))
                db.session.commit()
                rooms = db.session.query(Room).all()

            new_screenings = []
            now = datetime.now()
            monday = (now - timedelta(days=now.weekday())).replace(
                hour=14, minute=0, second=0, microsecond=0
            )

            for idx, movie in enumerate(movies):
                for day in range(7):
                    s_date = monday + timedelta(days=day, hours=idx)
                    new_screenings.append(
                        Screening(
                            movie_id=movie.id,
                            price=2500,
                            room_id=rooms[idx % len(rooms)].id,
                            screening_date=s_date
                        )
                    )

            db.session.add_all(new_screenings)
            db.session.commit()
            return True, "Test data added successfully"

        except Exception:
            db.session.rollback()
            return False, "Error adding test data"