import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.user_service import UserService
from tests.testing_helper import SetupHelper

client = TestClient(app)


class TestLogin:
    """
    Tests for /login endpoint.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        self.db = test_db
        self.service = UserService(self.db)
        self.user_email = "user1@test.com"
        self.password = "password123"
        SetupHelper.create_test_user(self.service, self.user_email, self.password)

    def test_login_success(self):
        """
        Test successful login with valid credentials.
        """
        response = client.post(
            "user/login",
            json={
                "email": self.user_email,
                "password": self.password,
            },
        )

        assert response.status_code == 200
        assert "access_token" in response.json()["detail"]

    def test_login_failure_wrong_password(self):
        """
        Test failed login with a wrong password for existing user.
        """
        response = client.post(
            "/user/login/",
            json={"email": self.user_email, "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert response.json() == {
            "detail": {
                "error": {"code": "AUTH_ERROR", "message": "Invalid email or password"}
            }
        }

    def test_login_failure_wrong_email(self):
        """
        Test failed login with a wrong email.
        """
        response = client.post(
            "/user/login/",
            json={"email": "user@example.com", "password": self.password},
        )

        assert response.status_code == 401
        assert response.json() == {
            "detail": {
                "error": {"code": "AUTH_ERROR", "message": "Invalid email or password"}
            }
        }

    def test_login_failure_no_existing_user(self):
        """
        Test failed login with no existing user.
        """
        response = client.post(
            "/user/login/",
            json={
                "email": "noexistingemail@test.com",
                "password": "wrongpassword",
            },
        )

        assert response.status_code == 401
        assert response.json() == {
            "detail": {
                "error": {"code": "AUTH_ERROR", "message": "Invalid email or password"}
            }
        }

    def test_invalid_email(self):
        """
        Test failed login with an invalid email format.
        """
        response = client.post(
            "/user/login/",
            json={"email": "testexample.com", "password": "wrongpassword"},
        )

        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["error"]["message"]
            == "Error in field 'email': value is not a valid email address: An email address must have an @-sign."
        )

    def test_without_password(self):
        """
        Test failed login without a password in the request body.
        """
        response = client.post("/user/login/", json={"email": "test@example.com"})
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["error"]["message"]
            == "Error in field 'password': Field required"
        )

    def test_without_email(self):
        """
        Test failed login without an email in the request body.
        """
        response = client.post("/user/login/", json={"password": self.password})
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["error"]["message"]
            == "Error in field 'email': Field required"
        )
