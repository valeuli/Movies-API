common_request_error_response = {
    "description": "Error during request to the external World Time API.",
    "content": {
        "application/json": {
            "example": {
                "error": {
                    "code": "REQUEST_ERROR",
                    "message": "Error during request to http://worldtimeapi.org/api/timezone/area/location.",
                }
            }
        }
    },
}

common_time_example = {
    "datetime": "2025-01-13T01:40:51.245747-04:00",
    "utc_datetime": "2025-01-13T05:40:51.245747+00:00",
    "utc_offset": "-04:00",
}

get_time_responses = {
    200: {
        "description": "Time data retrieved successfully.",
        "content": {
            "application/json": {
                "example": common_time_example,
            }
        },
    },
    502: common_request_error_response,
}
