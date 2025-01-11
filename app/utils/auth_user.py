from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.utils.jwt_handler import decode_access_token


def get_current_user(token: str, session_database):
    """
    Validates the JWT token and retrieves the current user.
    Returns None if the token is invalid or the user does not exist in the database.
    """
    payload = decode_access_token(token)
    if payload is None:
        return None

    email = payload.get("email")
    if email is None:
        return None

    user_service = UserService(session_database)
    user = user_service.get_user_by_email(email)

    return user


def validate_current_user(token: str, db: Session):
    """
    Validates the current user using the provided token.
    """
    current_user = get_current_user(token, db)
    if not current_user:
        content = {
            "error": {
                "code": "UNAUTHORIZED",
                "message": "You are not authorized to perform this action.",
            }
        }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=content,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
