import pytest
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.utils.auth_user import validate_current_user, get_current_user
from app.utils.jwt_handler import create_access_token
from tests.testing_helper import SetupHelper


class TestValidateCurrentUser:
    """
    Tests for validate_current_user function.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db: Session):
        """
        Initial configuration for every test.
        """
        self.session_db = test_db

    def test_validate_current_user_valid(self):
        """
        Test to validate a user with a valid token.
        """
        user_service = UserService(db=self.session_db)
        user_email = "user@example.com"
        password = "password."
        created_user = SetupHelper.create_test_user(user_service, user_email, password)
        token_user = create_access_token({"email": user_email})
        result = validate_current_user(token_user, self.session_db)
        assert result == created_user

    def test_validate_current_user_invalid_token(self):
        """
        Test to validate a user with an invalid token.
        """
        with pytest.raises(HTTPException) as exception_info:
            validate_current_user("invalid_token", self.session_db)

        assert exception_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exception_info.value.detail["error"]["code"] == "UNAUTHORIZED"

    def test_validate_current_user_no_token(self):
        """
        Test to validate a user with no token.
        """
        with pytest.raises(HTTPException) as exception_info:
            validate_current_user("", self.session_db)

        assert exception_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exception_info.value.detail["error"]["code"] == "UNAUTHORIZED"


class TestGetCurrentUser:
    """
    Tests for get_current_user function.
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db: Session):
        """
        Initial configuration for every test.
        """
        self.session_db = test_db
        self.user_service = UserService(db=self.session_db)
        self.user_email = "user1@example.com"
        self.password = "secure_password"
        self.created_user = SetupHelper.create_test_user(
            self.user_service, self.user_email, self.password
        )

    def test_get_current_user_valid_token_and_user_exists(self):
        """
        Test to valid token and the user exists in the database.
        """
        valid_token = create_access_token({"email": self.user_email})
        result = get_current_user(valid_token, self.session_db)

        assert result == self.created_user

    def test_get_current_user_invalid_token(self):
        """
        Test to try to get a user with an invalid token.
        """
        result = get_current_user("invalid_token", self.session_db)

        assert result is None

    def test_get_current_user_user_not_found(self):
        """
        Test with a valid token, but user does not exist in the database.
        """
        valid_token = create_access_token({"email": "user2@example.com"})
        result = get_current_user(valid_token, self.session_db)

        assert result is None

    def test_get_current_user_missing_email_in_token(self):
        """
        Test with a valid token, but 'email' is missing in the payload.
        """
        valid_token = create_access_token({"sub": "user2@example.com"})
        result = get_current_user(valid_token, self.session_db)

        assert result is None
