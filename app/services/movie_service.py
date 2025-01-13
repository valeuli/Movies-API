from sqlalchemy.orm import Session

from app.repositories.get_repository import get_repository
from app.models.movie import Movie


class MovieService:
    def __init__(self, db: Session):
        self.repository = get_repository(db, Movie)
