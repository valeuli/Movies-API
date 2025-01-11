from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.services.crud_service import CRUDService


class MovieService(CRUDService[Movie]):
    def __init__(self, db: Session):
        super().__init__(db, Movie)
