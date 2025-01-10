import pytest
from sqlalchemy.orm import Session

from app.database_settings import SessionLocal
from app.main import app
from app.services.user_service import UserService
from tests.testing_helper import SetupHelper


class TestUserService:
    """
    Unit tests for UserService.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db: Session) -> None:
        """
        Initial configuration for every test.
        """
        # Mock de la sesión de base de datos
        app.dependency_overrides[SessionLocal] = lambda: test_db
        self.db = test_db
        self.user_service = UserService(db=self.db)
        self.user_email = "user1@test.com"
        self.password = "password123"
        self.created_user = SetupHelper.create_test_user(
            self.user_service, self.user_email, self.password
        )

    def test_get_user_by_email_found(self):
        """
        Test to verify that it returns a user when the email exists.
        """
        result = self.user_service.get_user_by_email(self.user_email)
        assert result == self.created_user

    def test_get_user_by_email_not_found(self):
        """
        Test to verify that it returns None when the email does not exist.
        """
        result = self.user_service.get_user_by_email("nonexistent@example.com")
        assert result is None
