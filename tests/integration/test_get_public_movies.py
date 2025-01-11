import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.movie_service import MovieService
from app.services.user_service import UserService
from app.utils.jwt_handler import create_access_token
from tests.testing_helper import SetupHelper

client = TestClient(app)


class TestGetPublicMovies:
    """
    Tests for the get_public_movies endpoint.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """
        Initial configuration for every test.
        """
        self.test_db = test_db
        self.movie_service = MovieService(self.test_db)

        self.movies = [
            {
                "title": f"Private Movie {i}",
                "description": f"Description {i}",
                "publication_year": 2000 + i,
                "genre": "ACTION",
                "rating": 7.0 + i,
                "is_public": True if i % 2 == 0 else False,
                "user_id": 1,
            }
            for i in range(1, 11)
        ]

        for movie in self.movies:
            MovieService.create_object(self.movie_service, movie)

    def test_get_public_movies_default_pagination(self):
        """
        Test to retrieve public movies with default pagination.
        """
        response = client.get("movie/public")
        assert response.status_code == 200

        movies = response.json()
        assert len(movies) < 12
        for movie in movies:
            assert movie["is_public"] is True

    def test_get_public_movies_authenticated_user(self):
        user_email = "movie_user@example.com"
        password = "password123"
        SetupHelper.create_test_user(UserService(self.test_db), user_email, password)
        valid_token = create_access_token({"email": user_email})
        headers = {"Authorization": f"Bearer {valid_token}"}

        response = client.get("movie/public", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) > 1

    def test_get_public_movies_with_pagination(self):
        """
        Test to retrieve public movies with specific pagination.
        """
        response = client.get("movie/public?page=1&page_size=2")
        assert response.status_code == 200

        movies = response.json()
        assert len(movies) == 2

    def test_get_public_movies_out_of_bounds(self):
        """
        Test retrieving a page that exceeds the available movies.
        """
        response = client.get("movie/public?page=10&page_size=5")
        assert response.status_code == 200

        movies = response.json()
        assert len(movies) == 0

    def test_get_public_movies_invalid_page(self):
        """
        Test retrieving public movies with an invalid page parameter.
        """
        response = client.get("movie/public?page=-1&page_size=2")
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["error"]["message"]
            == "Error in field 'page': Input should be greater than or equal to 1"
        )

    def test_get_public_movies_invalid_page_size(self):
        """
        Test retrieving public movies with an invalid page size parameter.
        """
        response = client.get("movie/public?page=1&page_size=101")
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["error"]["message"]
            == "Error in field 'page_size': Input should be less than or equal to 100"
        )
