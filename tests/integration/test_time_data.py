from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from main import app
from app.routers.time_data import time_router

app.include_router(time_router, prefix="/time")

client = TestClient(app)


class TestGetTimeEndpoint:
    """
    Tests for the `get_time` endpoint.
    """

    @pytest.fixture(autouse=True)
    def septup(self):
        self.test_url = "/time/America/Bogota"

    @patch("app.routers.time_data.get_with_retry")
    def test_get_time_success(self, mock_get_with_retry):
        """
        Test that the endpoint returns correct data.
        """
        mock_response = {
            "datetime": "2025-01-01T12:00:00-05:00",
            "utc_datetime": "2025-01-01T17:00:00+00:00",
            "utc_offset": "-05:00",
        }
        mock_get_with_retry.return_value = mock_response
        response = client.get(self.test_url)

        assert response.status_code == 200
        assert response.json() == mock_response

    @patch("app.routers.time_data.get_with_retry")
    def test_get_time_with_region_success(self, mock_get_with_retry):
        """
        Test that the endpoint returns correct data with a region.
        """
        test_url = "/time/America/Argentina?region=Salta"
        mock_response = {
            "datetime": "2025-01-01T12:00:00-03:00",
            "utc_datetime": "2025-01-01T15:00:00+00:00",
            "utc_offset": "-03:00",
        }
        mock_get_with_retry.return_value = mock_response
        response = client.get(test_url)

        assert response.status_code == 200
        assert response.json() == mock_response
        mock_get_with_retry.assert_called_once_with(
            "http://worldtimeapi.org/api/timezone/America/Argentina/Salta"
        )

    @patch("app.routers.time_data.get_with_retry")
    def test_get_time_failure(self, mock_get_with_retry):
        """
        Test that the endpoint returns an error.
        """
        mock_get_with_retry.side_effect = Exception("Connection error")

        response = client.get(self.test_url)
        assert response.status_code == 502
        assert response.json() == {
            "detail": {
                "error": {
                    "code": "REQUEST_ERROR",
                    "message": "Error during request to http://worldtimeapi.org/api/timezone/America/Bogota.",
                }
            }
        }
