from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database_settings import SessionLocal
from app.schemas.movie import MovieCreate, MovieResponse
from app.services.movie_service import MovieService
from app.utils.auth_user import validate_current_user, get_current_user

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login",
)
movie_router = APIRouter()


@movie_router.post(
    "/create",
    status_code=201,
    response_model=MovieResponse,
    responses={
        201: {"description": "A new movie was successfully created."},
        401: {
            "description": "User does not have permission to perform this action. Needs authentication."
        },
        422: {"description": "The body of the request is missing a required field."},
    },
)
def create_movie(
    movie_data: MovieCreate,
    token: str = Depends(oauth2_scheme),
):
    """
    Creates a new movie associated with the authenticated user.
    The movie can be private or public.
    """
    session_database = SessionLocal()
    current_user = get_current_user(token, session_database)
    if not current_user:
        detail = {
            "error": {
                "code": "UNAUTHORIZED",
                "message": "You are not authorized to perform this action.",
            }
        }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    movi_service = MovieService(session_database)
    movie_data_dict = movie_data.model_dump()
    movie_data_dict["user_id"] = current_user.id

    new_movie = movi_service.create_object(movie_data_dict)
    return new_movie


@movie_router.get("/public", response_model=List[MovieResponse])
def get_public_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """
    Retrieve all public movies with pagination.
    """
    session_database = SessionLocal()
    movi_service = MovieService(session_database)
    offset = (page - 1) * page_size
    public_movies = movi_service.get_objects_by_filters(
        filters={"is_public": True},
        offset=offset,
        limit=page_size,
    )
    return public_movies


@movie_router.get("/user", response_model=List[MovieResponse])
def get_user_movies(
    token: str = Depends(oauth2_scheme),
    is_public: bool = Query(
        None,
        description="Filter movies by visibility: True for public, False for private.",
    ),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """
    Retrieve all movies public and private created by the authenticated user.
    """
    session_database = SessionLocal()
    current_user = validate_current_user(token, session_database)
    filters = {"user_id": current_user.id}
    if is_public is not None:
        filters["is_public"] = is_public

    movie_service = MovieService(session_database)
    offset = (page - 1) * page_size
    user_movies = movie_service.get_objects_by_filters(
        filters=filters,
        offset=offset,
        limit=page_size,
    )

    return user_movies


@movie_router.put("/{movie_id}", response_model=MovieResponse)
def update_private_movie(
    movie_id: int,
    movie_data: dict,
    token: str = Depends(oauth2_scheme),
):
    """
    Update at least one field of a private movie owned by the authenticated user.
    """
    session_database = SessionLocal()
    current_user = validate_current_user(token, session_database)

    movie_service = MovieService(session_database)
    movie = movie_service.get_object(movie_id)

    if not movie:
        detail = {
            "error": {
                "code": "NOT_FOUND",
                "message": "Movie not found.",
            }
        }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    if not movie.is_public and movie.user_id != current_user.id:
        detail = {
            "error": {
                "code": "UNAUTHORIZED",
                "message": "You are not authorized to perform this action.",
            }
        }
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

    updated_movie = movie_service.update_object(movie_id, movie_data)
    return updated_movie


@movie_router.delete("/{movie_id}/delete", status_code=204)
def delete_movie(
    movie_id: int,
    token: str = Depends(oauth2_scheme),
):
    """
    Delete a private movie owned by the authenticated user.
    """
    session_database = SessionLocal()
    current_user = validate_current_user(token, session_database)

    movie_service = MovieService(session_database)
    movie = movie_service.get_object(movie_id)

    if not movie:
        detail = {
            "error": {
                "code": "NOT_FOUND",
                "message": "Movie not found.",
            }
        }

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    if movie.user_id != current_user.id:
        detail = {
            "error": {
                "code": "UNAUTHORIZED",
                "message": "You are not authorized to perform this action.",
            }
        }
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

    movie_service.delete_object(movie_id)
    return {"detail": "Movie deleted successfully"}
