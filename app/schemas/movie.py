from datetime import datetime

from pydantic import BaseModel

from app.models.movie import GenreEnum


class MovieCreate(BaseModel):
    title: str
    description: str
    publication_year: int
    genre: GenreEnum
    rating: float
    is_public: bool


class MovieResponse(BaseModel):
    id: str | int
    title: str
    description: str
    publication_year: int
    genre: GenreEnum
    rating: float
    is_public: bool
    user_id: str | int | None
    created_at: datetime

    class ConfigDict:
        from_attributes = True
