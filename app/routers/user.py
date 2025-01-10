from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.database_settings import SessionLocal
from app.schemas.login import Login
from app.schemas.user import User
from app.services.user_service import UserService
from app.utils.jwt_handler import create_access_token
from app.utils.password_hasher import BcryptPasswordHasher

user_router = APIRouter()


@user_router.post("/login", status_code=200)
def login(login_data: Login):
    """
    Authenticates a user and returns a JWT access token if the credentials are valid.
    """
    db = SessionLocal()
    service = UserService(db)

    user = service.get_user_by_email(login_data.email)
    if not user or not BcryptPasswordHasher.verify_password(
        login_data.password, user.password
    ):
        content = {
            "error": {"code": "AUTH_ERROR", "message": "Invalid email or password"}
        }
        return JSONResponse(content=content, status_code=401)

    access_token = create_access_token(data={"sub": user.email})
    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}, status_code=200
    )


@user_router.post("/create", status_code=201)
def create_user(user_data: User):
    """
    Creates a new user if they are not already registered.
    """
    db = SessionLocal()
    service = UserService(db)
    existing_user = service.get_user_by_email(user_data.email)
    if existing_user:
        content = {
            "error": {"code": "USER_ALREADY_EXISTS", "message": "User already exists."}
        }
        return JSONResponse(content=content, status_code=400)

    user_data.password = BcryptPasswordHasher.hash_password(user_data.password)
    service.create_object(user_data.model_dump())
    return JSONResponse(content={"msg": "User created"}, status_code=201)
