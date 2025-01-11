import os
from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.utils.jwt_handler import create_access_token, decode_access_token


class TestCreateAccessToken:
    """
    Tests for the create_access_token function.
    """

    def test_create_access_token_returns_token(self):
        """
        Test to create a valid JWT token.
        """
        data = {"email": "test_user"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_expiration(self):
        """
        Test to verify that the token expires as expected.
        """
        data = {"email": "test_user"}
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
        data = {"email": "test_user"}
        token = create_access_token(data)

        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(
                token,
                "wrong_secret_key",
                algorithms=[os.environ["ALGORITHM"]],
            )


class TestDecodeAccessToken:
    """
    Tests for decode_access_token function.
    """

    def test_decode_valid_token(self):
        """
        Test decoding a valid JWT token.
        """
        token_data = {"email": "user@example.com"}
        valid_token = create_access_token(token_data)
        decoded_payload = decode_access_token(valid_token)

        assert decoded_payload is not None
        assert decoded_payload["email"] == "user@example.com"
        assert "exp" in decoded_payload

    def test_decode_expired_token(self):
        """
        Test to decode an expired JWT token.
        """
        expired_data = {
            "email": "user@example.com",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=10),
        }
        expired_token = jwt.encode(
            expired_data, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"]
        )

        decoded_payload = decode_access_token(expired_token)
        assert decoded_payload is None

    def test_decode_invalid_token_signature(self):
        """
        Test decoding a token with an invalid signature.
        """
        invalid_token = jwt.encode(
            {
                "email": "user@example.com",
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            },
            "wrong_secret",  # Firma incorrecta
            algorithm=os.environ["ALGORITHM"],
        )
        decoded_payload = decode_access_token(invalid_token)

        assert decoded_payload is None

    def test_decode_malformed_token(self):
        """
        Test decoding a malformed JWT token.
        """
        malformed_token = "this.is.not.a.jwt"
        decoded_payload = decode_access_token(malformed_token)
        assert decoded_payload is None
