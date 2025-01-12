from fastapi import APIRouter, HTTPException

from app.utils.get_with_retry import get_with_retry

time_router = APIRouter()
WORLD_TIME_API_URL = "http://worldtimeapi.org/api/timezone"


@time_router.get("/{area}/{location}", status_code=200)
def get_time(area: str, location: str, region: str = None):
    """
    Retrieves time data for an area/location and an optional parameter region.
    """
    url_parts = [WORLD_TIME_API_URL, area, location]
    if region:
        url_parts.append(region)

    world_time_url = "/".join(url_parts)

    try:
        time_data = get_with_retry(world_time_url)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail={
                "error": {
                    "code": "REQUEST_ERROR",
                    "message": f"Error during request to {world_time_url}.",
                }
            },
        )

    result = {
        "datetime": time_data.get("datetime"),
        "utc_datetime": time_data.get("utc_datetime"),
        "utc_offset": time_data.get("utc_offset"),
    }

    return result
