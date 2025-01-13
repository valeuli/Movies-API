import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.movie_service import MovieService
from app.services.user_service import UserService
from app.utils.jwt_handler import create_access_token
from tests.testing_helper import SetupHelper

client = TestClient(app)


class TestDeleteMovie:
    """
    Tests for the delete_movie endpoint.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """
        Initial configuration for every test.
        """
        self.db = test_db
        self.user_service = UserService(self.db)
        self.user_email = "testuser@example.com"
        self.password = "password123"
        self.test_user = SetupHelper.create_test_user(
            self.user_service, self.user_email, self.password
        )
        self.valid_token = create_access_token({"email": self.user_email})

        self.movie_service = MovieService(self.db)
        self.movie = self.movie_service.repository.create_object(
            {
                "title": "Test Movie",
                "description": "A private romantic movie.",
                "publication_year": 2025,
                "genre": "ROMANCE",
                "rating": 10,
                "is_public": False,
                "user_id": self.test_user.id,
            },
        )

    def test_delete_movie_not_found(self):
        """
        Test deleting a movie that does not exist.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}

        response = client.delete("movie/0/delete", headers=headers)
        error_detail = response.json()["detail"]["error"]

        assert response.status_code == 404
        assert error_detail["code"] == "NOT_FOUND"
        assert error_detail["message"] == "Movie not found."

    def test_delete_movie_unauthorized_user(self):
        """
        Test deleting a private movie that belongs to another user.
        """
        other_user = SetupHelper.create_test_user(
            self.user_service, "del_user@example.com"
        )
        other_user_token = create_access_token({"email": other_user.email})

        headers = {"Authorization": f"Bearer {other_user_token}"}
        response = client.delete(f"movie/{self.movie.id}/delete", headers=headers)

        error_detail = response.json()["detail"]["error"]
        assert response.status_code == 403
        assert error_detail["code"] == "UNAUTHORIZED"
        assert (
            error_detail["message"] == "You are not authorized to perform this action."
        )

    def test_delete_movie_no_authentication(self):
        """
        Test deleting a private movie without authentication.
        """
        response = client.delete(f"movie/{self.movie.id}/delete")

        error_detail = response.json()["detail"]
        assert response.status_code == 401
        assert error_detail == "Not authenticated"

    def test_delete_movie_success(self):
        """
        Test successful deletion of a private movie owned.
        """
        headers = {"Authorization": f"Bearer {self.valid_token}"}
        response = client.delete(f"movie/{self.movie.id}/delete", headers=headers)
        movie_in_db = self.movie_service.repository.get_object(self.movie.id)

        assert response.status_code == 204
        assert response.text == ""
        assert movie_in_db is None
