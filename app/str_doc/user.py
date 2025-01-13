common_user_already_exists_response = {
    "description": "The user is already registered.",
    "content": {
        "application/json": {
            "example": {
                "error": {
                    "code": "USER_ALREADY_EXISTS",
                    "message": "User already exists",
                }
            }
        }
    },
}

common_auth_error_response = {
    "description": "Authentication error due to invalid email or password.",
    "content": {
        "application/json": {
            "example": {
                "error": {
                    "code": "AUTH_ERROR",
                    "message": "Invalid email or password",
                }
            }
        }
    },
}

common_user_created_response = {
    "description": "User created successfully.",
    "content": {"application/json": {"example": {"detail": "User created"}}},
}

common_access_token_response = {
    "description": "Access token generated successfully.",
    "content": {
        "application/json": {
            "example": {
                "detail": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                }
            }
        }
    },
}

create_user_responses = {
    201: common_user_created_response,
    400: common_user_already_exists_response,
}

login_responses = {
    200: common_access_token_response,
    401: common_auth_error_response,
}
