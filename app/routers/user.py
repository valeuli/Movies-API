from fastapi import APIRouter, HTTPException

from app.database_settings import SessionLocal
from app.schemas.login import Login
from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.utils.jwt_handler import create_access_token
from app.utils.password_hasher import BcryptPasswordHasher

user_router = APIRouter()


@user_router.post(
    "/create",
    status_code=201,
)
def create_user(user_data: UserCreate):
    """
    Creates a new user if they are not already registered.
    """
    session_database = SessionLocal()
    service = UserService(session_database)
    existing_user = service.get_user_by_email(user_data.email)
    if existing_user:
        detail = {
            "error": {"code": "USER_ALREADY_EXISTS", "message": "User already exists"},
        }
        raise HTTPException(status_code=400, detail=detail)
    user_data.password = BcryptPasswordHasher.hash_password(user_data.password)
    service.repository.create_object(user_data.model_dump())
    return {"detail": "User created"}


@user_router.post("/login", status_code=200)
def login(login_data: Login):
    """
    Authenticates a user and returns a JWT access token if the credentials are valid.
    """
    session_database = SessionLocal()
    service = UserService(session_database)

    user = service.get_user_by_email(login_data.email)
    if not user or not BcryptPasswordHasher.verify_password(
        login_data.password, user.password
    ):
        detail = {
            "error": {"code": "AUTH_ERROR", "message": "Invalid email or password"}
        }
        raise HTTPException(status_code=401, detail=detail)

    access_token = create_access_token(data={"email": user.email})
    content = {"detail": {"access_token": access_token, "token_type": "bearer"}}
    return content
