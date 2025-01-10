import jwt
import pytest
import os
from datetime import datetime, timedelta, timezone
from app.utils.jwt_handler import create_access_token

os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "5"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["ALGORITHM"] = "HS256"


class TestCreateAccessToken:
    """
    Tests for the create_access_token function.
    """

    def test_create_access_token_returns_token(self):
        """
        Test to create a valid JWT token.
        """
        data = {"sub": "test_user"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_expiration(self):
        """
        Test to verify that the token expires as expected.
        """
        data = {"sub": "test_user"}
        token = create_access_token(data)
        decoded = jwt.decode(
            token,
            os.environ["SECRET_KEY"],
            algorithms=[os.environ["ALGORITHM"]],
        )

        expected_expiration = (
            datetime.now(timezone.utc)
            + timedelta(minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
        ).replace(tzinfo=timezone.utc, microsecond=0)
        token_exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)

        delta = abs((expected_expiration - token_exp).total_seconds())
        assert delta < 1

    def test_create_access_token_invalid_key(self):
        """
        Test to verify that decoding the token with an incorrect key results in an error.
        """
        data = {"sub": "test_user"}
        token = create_access_token(data)

        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(
                token,
                "wrong_secret_key",
                algorithms=[os.environ["ALGORITHM"]],
            )
