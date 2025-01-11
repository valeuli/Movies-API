import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv()


def create_access_token(data: dict) -> str:
    """
    Returns JWT token for login.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"]
    )


def decode_access_token(token: str) -> dict | None:
    """
    Decodes and validates a JWT token, returning a dict or None if the token is invalid.
    """
    try:
        payload = jwt.decode(
            token,
            os.environ["SECRET_KEY"],
            algorithms=[os.environ["ALGORITHM"]],
        )
        return payload
    except jwt.exceptions.PyJWTError as e:
        return None
