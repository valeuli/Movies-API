import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.main import app
from app.services.user_service import UserService
from app.utils.jwt_handler import create_access_token
from tests.testing_helper import SetupHelper

client = TestClient(app)


class TestCreateMovie:
    """
    Tests for the create_movie endpoint.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        self.db = test_db
        self.user_service = UserService(self.db)

        self.user_email = "testuser@example.com"
        self.password = "password123"
        SetupHelper.create_test_user(self.user_service, self.user_email, self.password)
        self.valid_token = create_access_token({"email": self.user_email})

        self.movie_data = {
            "title": "Inception",
            "description": "A mind-bending thriller",
            "publication_year": 2010,
            "genre": "Sci-Fi",
            "rating": 8.8,
            "is_public": True,
        }

    def test_create_movie_success(self):
        """
        Test successful creation of a movie.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}

        response = client.post("/movie/create", json=self.movie_data, headers=headers)
        response_data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert response_data["title"] == self.movie_data["title"]
        assert response_data["description"] == self.movie_data["description"]
        assert response_data["user_id"] is not None

    def test_create_movie_unauthenticated(self):
        """
        Test creating a movie without authentication (no token).
        """
        response = client.post("/movie/create", json=self.movie_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Not authenticated"

    def test_create_movie_missing_required_field(self):
        """
        Test creating a movie with missing required fields.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}
        incomplete_movie_data = self.movie_data
        incomplete_movie_data.pop("title")
        response = client.post(
            "/movie/create", json=incomplete_movie_data, headers=headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "detail" in response.json()

    def test_create_movie_invalid_token(self):
        """
        Test creating a movie with an invalid token.
        """
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/movie/create", json=self.movie_data, headers=headers)

        detail_response = response.json()["detail"]
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            detail_response["error"]["message"]
            == "You are not authorized to perform this action."
        )
