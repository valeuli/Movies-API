import pytest
from fastapi.testclient import TestClient
from main import app
from app.services.movie_service import MovieService
from app.services.user_service import UserService
from app.utils.jwt_handler import create_access_token
from tests.testing_helper import SetupHelper

client = TestClient(app)


class TestGetUserMovies:
    """
    Unit tests for the get_user_movies endpoint.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """
        Initial configuration for every test.
        """
        self.db = test_db

        self.user_service = UserService(self.db)

        self.test_user = SetupHelper.create_test_user(self.user_service)
        self.valid_token = create_access_token({"email": self.test_user.email})

        self.movie_service = MovieService(self.db)
        self.user_movies = [
            {
                "title": f"Movie {i}",
                "description": f"Description {i}",
                "publication_year": 2000 + i,
                "genre": "SCIFI",
                "rating": 8.0 + i * 0.1,
                "is_public": i % 2 == 0,
                "user_id": self.test_user.id,
            }
            for i in range(1, 11)
        ]

        for movie in self.user_movies:
            self.movie_service.repository.create_object(movie)

    def test_get_user_movies_all(self):
        """
        Test to retrieve all movies, public and private created by the authenticated user.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}
        response = client.get("/movie/user", headers=headers)

        movies = response.json()
        assert response.status_code == 200
        assert len(movies) == len(self.user_movies)

    def test_get_user_movies_public_only(self):
        """
        Test to verify that the filter only works for public movies created by the authenticated user.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}
        response = client.get("/movie/user?is_public=true", headers=headers)

        movies = response.json()
        assert response.status_code == 200
        for movie in movies:
            assert movie["is_public"] is True

    def test_get_user_movies_private_only(self):
        """
        Test to retrieve only private movies created by the authenticated user.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}
        response = client.get("/movie/user?is_public=false", headers=headers)

        movies = response.json()
        assert response.status_code == 200
        for movie in movies:
            assert movie["is_public"] is False

    def test_get_user_movies_with_pagination(self):
        """
        Test to retrieve movies with specific pagination.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}
        response = client.get("/movie/user?page=1&page_size=5", headers=headers)

        movies = response.json()
        assert response.status_code == 200
        assert len(movies) == 5

    def test_get_user_movies_unauthenticated(self):
        """
        Test to retrieve movies without authentication.
        """
        response = client.get("/movie/user")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"
