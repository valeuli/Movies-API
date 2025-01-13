import random
from datetime import datetime, timezone

from app.database_settings import engine, SessionLocal, Base
from app.models.user import User
from app.models.movie import Movie, GenreEnum

Base.metadata.create_all(bind=engine)


def create_movies():
    """
    Create 15 public movies and save them to the database.
    """
    titles = [
        "The Shawshank Redemption",
        "The Godfather",
        "The Dark Knight",
        "Pulp Fiction",
        "The Lord of the Rings: The Return of the King",
        "Forrest Gump",
        "Inception",
        "Fight Club",
        "The Matrix",
        "Goodfellas",
        "The Silence of the Lambs",
        "Interstellar",
        "Se7en",
        "The Usual Suspects",
        "The Lion King",
    ]

    descriptions = [
        "A story of hope and friendship.",
        "A powerful tale of family and crime.",
        "A dark hero rises to save the city.",
        "Non-linear storytelling at its best.",
        "An epic journey to destroy the One Ring.",
        "A man's journey through life and love.",
        "A dream within a dream.",
        "A story about rebellion and freedom.",
        "A mind-bending sci-fi masterpiece.",
        "The rise and fall of a gangster.",
        "A psychological thriller of a lifetime.",
        "Exploring the boundaries of space and time.",
        "A gritty detective story.",
        "A twisty tale of deception.",
        "A heartwarming animated classic.",
    ]

    genres = list(GenreEnum)

    session = SessionLocal()
    try:
        for i in range(15):
            movie = Movie(
                title=titles[i],
                description=descriptions[i],
                publication_year=random.randint(1990, 2024),
                genre=random.choice(genres),
                rating=round(random.uniform(1.0, 10.0), 1),
                is_public=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            session.add(movie)

        session.commit()
        print("15 movies were successfully created and saved to the database.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    create_movies()
