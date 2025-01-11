import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    Float,
)
from sqlalchemy.orm import relationship

from app.database_settings import Base


class GenreEnum(enum.Enum):
    """
    Enum for movie genres.
    """

    ACTION = "Action"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    HORROR = "Horror"
    SCIFI = "Sci-Fi"
    ROMANCE = "Romance"
    THRILLER = "Thriller"
    FANTASY = "Fantasy"
    DOCUMENTARY = "Documentary"
    MUSICAL = "Musical"


class Movie(Base):
    """
    Movie model.
    """

    __tablename__ = "movie"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    publication_year = Column(Integer, nullable=False)
    genre = Column(Enum(GenreEnum), nullable=False)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_public = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="movies", lazy="joined", uselist=False)
