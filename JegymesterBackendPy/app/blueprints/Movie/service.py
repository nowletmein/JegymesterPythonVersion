from app.extensions import db
from app.models.movie import Movie
from app.blueprints.Movie.schemas import MovieResponseSchema
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.utils.date_utils import ensure_datetime

class MovieService:

    @staticmethod
    def get_all():
        stmt = select(Movie).options(selectinload(Movie.screenings))
        movies = db.session.execute(stmt).scalars().all()
        
        results = []
        for movie in movies:
            screenings_data = []
            for s in movie.screenings:
                screenings_data.append({
                    "id": s.id,
                    "movie_id": s.movie_id,
                    "room_id": s.room_id,
                    "price": s.price,
                    "screening_date": ensure_datetime(s.screening_date)
                })
            
            results.append({
                "id": movie.id,
                "title": movie.title,
                "director": movie.director,
                "description": movie.description,
                "length": movie.length,
                "pg": movie.pg,
                "rating": movie.rating,
                "picture_path": movie.picture_path,
                "screenings": screenings_data
            })
            
        return True, results

    @staticmethod
    def get_by_id(id):
        stmt = select(Movie).filter_by(id=id).options(selectinload(Movie.screenings))
        movie = db.session.execute(stmt).scalar_one_or_none()
        
        if not movie:
            return False, "Movie not found"

        screenings_data = []
        for s in movie.screenings:
            screenings_data.append({
                "id": s.id,
                "movie_id": s.movie_id,
                "room_id": s.room_id,
                "price": s.price,
                "screening_date": ensure_datetime(s.screening_date)
            })

        data = {
            "id": movie.id,
            "title": movie.title,
            "director": movie.director,
            "description": movie.description,
            "length": movie.length,
            "pg": movie.pg,
            "rating": movie.rating,
            "picture_path": movie.picture_path,
            "screenings": screenings_data
        }
        return True, data

    @staticmethod
    def create(json_data):
        try:
            existing = db.session.query(Movie).filter_by(
                title=json_data.get("title"), 
                director=json_data.get("director")
            ).first()
            
            if existing:
                return False, "Movie with this name and director already exists"

            movie = Movie(**json_data)
            db.session.add(movie)
            db.session.commit()
            return True, movie.id
        except Exception:
            db.session.rollback()
            return False, "Error creating movie"

    @staticmethod
    def delete(movie_id):
        movie = db.session.get(Movie, movie_id)
        if not movie:
            return False, "Movie with this ID does not exist"
        
        db.session.delete(movie)
        db.session.commit()
        return True, 0

    @staticmethod
    def edit(movie_id, json_data):
        try:
            movie = db.session.get(Movie, movie_id)
            if not movie:
                return False, "Movie not found"

            for key, value in json_data.items():
                if value is not None and value != "" and value != "string" and value != 0:
                    if hasattr(movie, key):
                        setattr(movie, key, value)

            db.session.commit()
            return MovieService.get_by_id(movie_id)
        except Exception:
            db.session.rollback()
            return False, "Error updating movie"

    @staticmethod
    def add_test_data():
        try:
            count = db.session.query(Movie).count()
            if count > 5:
                return True, "Data already exists"

            test_movies = [
                Movie(title="Civil War", director="Alex Garland", pg="16", length=109, description="A journey across a dystopian future America.", picture_path="/Frontend/my-app/public/content_img/civilwar.jpg", rating="7.1"),
                Movie(title="Ghostbusters: Frozen Empire", director="Gil Kenan", pg="12", length=115, description="The Spengler family returns to the iconic NYC firehouse.", picture_path="/Frontend/my-app/public/content_img/ghostbusters.jpg", rating="6.1"),
                Movie(title="Godzilla x Kong", director="Adam Wingard", pg="12", length=115, description="Two ancient titans face a colossal threat hidden within our world.", picture_path="/Frontend/my-app/public/content_img/godzilla.jpg", rating="6.4"),
                Movie(title="Kung Fu Panda 4", director="Mike Mitchell", pg="6", length=94, description="Po is tapped to become the Spiritual Leader of the Valley of Peace.", picture_path="/Frontend/my-app/public/content_img/panda.jpg", rating="6.7"),
                Movie(title="Dűne: Második rész", director="Denis Villeneuve", pg="16", length=166, description="Paul Atreides unites with Chani and the Fremen while on a warpath of revenge.", picture_path="/Frontend/my-app/public/content_img/dune2.jpg", rating="8.5")
            ]

            db.session.add_all(test_movies)
            db.session.commit()
            return True, "Test data added successfully"
        except Exception:
            db.session.rollback()
            return False, "Error adding test data"