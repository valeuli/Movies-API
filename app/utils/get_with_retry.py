from typing import Optional, Dict

import requests
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_with_retry(
    url: str,
    data: Optional[Dict] = None,
    headers: Optional[Dict] = None,
) -> dict | None:
    """
    Makes an HTTP request with retry logic.
    """

    response = requests.get(
        url=url,
        json=data,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()
