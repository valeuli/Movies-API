import pytest
from fastapi.testclient import TestClient

from app.database_settings import SessionLocal
from app.main import app
from app.services.user_service import UserService
from app.utils.password_hasher import BcryptPasswordHasher
from tests.testing_helper import SetupHelper

client = TestClient(app)


class TestCreateUser:
    """
    Tests for the /create endpoint.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        app.dependency_overrides[SessionLocal] = lambda: test_db
        self.db = test_db
        self.service = UserService(self.db)
        self.password = "password123"
        self.user_email = "testuser@example.com"
        self.user_data = {
            "email": self.user_email,
            "password": self.password,
            "first_name": "John",
            "last_name": "Doe",
        }
        SetupHelper.create_test_user(self.service, self.user_email, self.password)

    def test_create_user_success(self):
        """
        Test successfully create a new user.
        """
        user_email = "testuser1@example.com"
        user_data = {
            "email": user_email,
            "password": self.password,
            "first_name": "Test",
            "last_name": "User",
        }
        response = client.post(
            "/user/create/",
            json=user_data,
        )

        assert response.status_code == 201
        assert response.json() == {"msg": "User created"}

        created_user = self.service.get_user_by_email(user_email)
        assert created_user is not None
        assert BcryptPasswordHasher.verify_password(
            self.password, created_user.password
        )

    def test_create_user_already_exists(self):
        """
        Test to try to create a user with an email that already exists.
        """
        response = client.post(
            "/user/create/",
            json=self.user_data,
        )

        assert response.status_code == 400
        assert response.json() == {
            "error": {"code": "USER_ALREADY_EXISTS", "message": "User already exists."}
        }

    def test_create_user_missing_email(self):
        """
        Test to create a user without providing an email in the body.
        """
        invalid_user_data = self.user_data.copy()
        invalid_user_data.pop("email")

        response = client.post(
            "/user/create/",
            json=invalid_user_data,
        )

        assert response.status_code == 422
        assert "email" in response.json()["detail"][0]["loc"]

    def test_create_user_invalid_email(self):
        """
        Test to create a user without providing an invalid email in the body.
        """
        invalid_user_data = self.user_data.copy()
        invalid_user_data["email"] = "testuserexample.com"

        response = client.post(
            "/user/create/",
            json=invalid_user_data,
        )

        assert response.status_code == 422
        assert "email" in response.json()["detail"][0]["loc"]

    def test_create_user_missing_password(self):
        """
        Test to create a user without a password in the body.
        """
        invalid_user_data = self.user_data.copy()
        invalid_user_data.pop("password")

        response = client.post(
            "/user/create/",
            json=invalid_user_data,
        )

        assert response.status_code == 422
        assert "password" in response.json()["detail"][0]["loc"]

    def test_create_user_missing_first_name(self):
        """
        Test to create a user without providing a first name in the body.
        """
        invalid_user_data = self.user_data.copy()
        invalid_user_data.pop("first_name")

        response = client.post(
            "/user/create/",
            json=invalid_user_data,
        )

        assert response.status_code == 422
        assert "first_name" in response.json()["detail"][0]["loc"]

    def test_create_user_missing_last_name(self):
        """
        Test to create a user without providing a last name in the body.
        """
        invalid_user_data = self.user_data.copy()
        invalid_user_data.pop("last_name")

        response = client.post(
            "/user/create/",
            json=invalid_user_data,
        )

        assert response.status_code == 422
        assert "last_name" in response.json()["detail"][0]["loc"]
