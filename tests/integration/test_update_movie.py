import pytest
from fastapi.testclient import TestClient

from main import app
from app.services.movie_service import MovieService
from app.services.user_service import UserService
from app.utils.jwt_handler import create_access_token
from tests.testing_helper import SetupHelper

client = TestClient(app)


class TestUpdatePrivateMovie:
    """
    Tests for the update_private_movie endpoint.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """
        Initial configuration for every test.
        """
        self.test_db = test_db
        self.user_service = UserService(self.test_db)
        self.user_email = "user_up@example.com"
        password = "password123"
        self.test_user = SetupHelper.create_test_user(
            self.user_service, self.user_email, password
        )
        self.valid_token = create_access_token({"email": self.user_email})
        self.movie_service = MovieService(self.test_db)
        self.movie = self.movie_service.repository.create_object(
            {
                "title": "Test Movie",
                "description": "Original Description",
                "publication_year": 2020,
                "genre": "COMEDY",
                "rating": 10,
                "is_public": False,
                "user_id": self.test_user.id,
            },
        )

    def test_update_private_movie_success(self):
        """
        Test to successfully update a private movie owned by the authenticated user.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}
        update_data = {"description": "Updated Description"}

        response = client.put(
            f"/movie/{self.movie.id}", json=update_data, headers=headers
        )

        assert response.status_code == 200
        updated_movie = response.json()
        assert updated_movie["id"] == self.movie.id
        assert updated_movie["description"] == "Updated Description"
        assert updated_movie["title"] == "Test Movie"

    def test_update_private_movie_not_found(self):
        """
        Test to try to update a movie that does not exist.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}
        update_data = {"description": "Updated Description"}
        response = client.put("movie/9999", json=update_data, headers=headers)

        assert response.status_code == 404
        error_detail = response.json()["detail"]
        assert error_detail["error"]["code"] == "NOT_FOUND"
        assert error_detail["error"]["message"] == "Movie not found."

    def test_update_private_movie_unauthorized_user(self):
        """
        Test updating a private movie that belongs to another user.
        """
        other_user_email = "otheruser@example.com"
        other_user_password = "password456"
        SetupHelper.create_test_user(
            self.user_service, other_user_email, other_user_password
        )
        other_user_token = create_access_token({"email": other_user_email})

        headers = {"Authorization": f"Bearer {other_user_token}"}
        update_data = {"description": "Updated Description"}

        response = client.put(
            f"movie/{self.movie.id}", json=update_data, headers=headers
        )

        assert response.status_code == 403
        error_detail = response.json()["detail"]
        assert error_detail["error"]["code"] == "UNAUTHORIZED"
        assert (
            error_detail["error"]["message"]
            == "You are not authorized to perform this action."
        )

    def test_update_private_movie_no_authentication(self):
        """
        Test updating a private movie without authentication.
        """
        update_data = {"description": "Updated Description"}
        movie_id = int(self.movie.id)
        response = client.put(f"movie/{movie_id}", json=update_data)

        assert response.status_code == 401
        error_detail = response.json()["detail"]
        assert error_detail == "Not authenticated"

    def test_update_private_movie_without_data(self):
        """
        Test to successfully update a private movie owned by the authenticated user.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}
        update_data = {}

        response = client.put(
            f"/movie/{self.movie.id}", json=update_data, headers=headers
        )
        error_detail = response.json()["detail"]

        assert response.status_code == 400
        assert error_detail["error"]["code"] == "MISSING"
        assert error_detail["error"]["message"] == "There is not data to update."
