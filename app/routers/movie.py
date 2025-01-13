from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database_settings import get_session_local
from app.schemas.movie import MovieCreate, MovieResponse
from app.services.movie_service import MovieService
from app.str_doc.movie import (
    create_movie_responses,
    movie_public_responses,
    movie_update_responses,
    movie_user_responses,
    movie_delete_responses,
)
from app.utils.auth_user import validate_current_user, get_current_user

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login",
)
movie_router = APIRouter()


@movie_router.post(
    "/create",
    status_code=201,
    response_model=MovieResponse,
    responses=create_movie_responses,
)
def create_movie(
    movie_data: MovieCreate,
    token: str = Depends(oauth2_scheme),
    session_database=Depends(get_session_local),
):
    """
    Creates a new movie associated with the authenticated user.
    The movie can be private or public.
    """
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
    new_movie = movi_service.repository.create_object(movie_data_dict)
    return new_movie


@movie_router.get(
    "/public", response_model=List[MovieResponse], responses=movie_public_responses
)
def get_public_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    session_database=Depends(get_session_local),
):
    """
    Retrieve all public movies with pagination.
    """
    movie_service = MovieService(session_database)
    offset = (page - 1) * page_size
    public_movies = movie_service.repository.get_objects_by_filters(
        filters={"is_public": True},
        offset=offset,
        limit=page_size,
    )
    if not public_movies:
        return []
    return movie_service.repository.to_schema(public_movies, MovieResponse)


@movie_router.get(
    "/user",
    response_model=List[MovieResponse],
    responses=movie_user_responses,
)
def get_user_movies(
    token: str = Depends(oauth2_scheme),
    is_public: bool = Query(
        None,
        description="Filter movies by visibility: True for public, False for private.",
    ),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    session_database=Depends(get_session_local),
):
    """
    Retrieve all movies public and private created by the authenticated user.
    """
    current_user = validate_current_user(token, session_database)
    filters = {"user_id": current_user.id}
    if is_public is not None:
        filters["is_public"] = is_public

    movie_service = MovieService(session_database)
    offset = (page - 1) * page_size
    user_movies = movie_service.repository.get_objects_by_filters(
        filters=filters,
        offset=offset,
        limit=page_size,
    )

    return movie_service.repository.to_schema(user_movies, MovieResponse)


@movie_router.put(
    "/{movie_id}", response_model=MovieResponse, responses=movie_update_responses
)
def update_private_movie(
    movie_id: int | str,
    movie_data: dict,
    token: str = Depends(oauth2_scheme),
    session_database=Depends(get_session_local),
):
    """
    Update at least one field of a private movie owned by the authenticated user.
    """
    if not movie_data:
        detail = {
            "error": {
                "code": "MISSING",
                "message": "There is not data to update.",
            }
        }
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
    current_user = validate_current_user(token, session_database)

    movie_service = MovieService(session_database)
    movie = movie_service.repository.get_object(movie_id)

    if not movie:
        detail = {
            "error": {
                "code": "NOT_FOUND",
                "message": "Movie not found.",
            }
        }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    movie_obj = movie_service.repository.to_schema(movie, MovieResponse)
    if not movie_obj.is_public and movie_obj.user_id != current_user.id:
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

    updated_movie = movie_service.repository.update_object(movie_id, movie_data)
    return movie_service.repository.to_schema(updated_movie, MovieResponse)


@movie_router.delete(
    "/{movie_id}/delete", status_code=204, responses=movie_delete_responses
)
def delete_movie(
    movie_id: int | str,
    token: str = Depends(oauth2_scheme),
    session_database=Depends(get_session_local),
):
    """
    Delete a private movie owned by the authenticated user.
    """
    current_user = validate_current_user(token, session_database)

    movie_service = MovieService(session_database)
    movie = movie_service.repository.get_object(movie_id)

    if not movie:
        detail = {
            "error": {
                "code": "NOT_FOUND",
                "message": "Movie not found.",
            }
        }

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    movie = movie_service.repository.to_schema(movie, MovieResponse)
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

    movie_service.repository.delete_object(movie_id)
    return {"detail": "Movie deleted successfully"}
