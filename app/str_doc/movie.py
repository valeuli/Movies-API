common_unauthorized_response = {
    "description": "User is not authenticated or token is invalid.",
    "content": {
        "application/json": {
            "example": {
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "You are not authorized to perform this action.",
                }
            }
        }
    },
}

common_not_found_response = {
    "description": "Resource not found.",
    "content": {
        "application/json": {
            "example": {
                "error": {
                    "code": "NOT_FOUND",
                    "message": "Movie not found.",
                }
            }
        }
    },
}

common_movie_example = {
    "id": 1,
    "title": "Inception",
    "description": "A mind-bending thriller",
    "publication_year": 2010,
    "genre": "Sci-Fi",
    "rating": 9.2,
    "is_public": True,
    "user_id": 123,
    "created_at": "2025-01-13T01:00:00Z",
    "updated_at": "2025-01-13T01:00:00Z",
}
create_movie_responses = {
    201: {
        "description": "A new movie was successfully created.",
        "content": {"application/json": {"example": common_movie_example}},
    },
    401: common_unauthorized_response,
    422: {
        "description": "Invalid input data. Missing required fields or validation error.",
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "code": "INVALID_DATA",
                        "message": "Validation error in request body.",
                    },
                    "detail": [
                        {
                            "loc": ["body", "title"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        }
                    ],
                }
            }
        },
    },
}

movie_public_responses = {
    200: {
        "description": "A list of public movies.",
        "content": {"application/json": {"example": [common_movie_example]}},
    },
}

movie_user_responses = {
    200: {
        "description": "A list of movies created by the authenticated user.",
        "content": {"application/json": {"example": [common_movie_example]}},
    },
    401: common_unauthorized_response,
}

movie_update_responses = {
    200: {
        "description": "Movie updated successfully.",
        "content": {
            "application/json": {
                "example": {
                    **common_movie_example,
                    "description": "Updated Description",
                    "updated_at": "2025-01-13T01:05:00Z",
                }
            }
        },
    },
    400: {
        "description": "No data provided for update.",
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "code": "MISSING",
                        "message": "There is no data to update.",
                    }
                }
            }
        },
    },
    403: common_unauthorized_response,
    404: common_not_found_response,
}

movie_delete_responses = {
    204: {"description": "Movie deleted successfully."},
    403: common_unauthorized_response,
    404: common_not_found_response,
}
