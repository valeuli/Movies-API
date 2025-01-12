from unittest.mock import patch, MagicMock

import pytest
from requests.exceptions import HTTPError

from app.utils.get_with_retry import get_with_retry


class TestGetWithRetry:
    """
    Tests for the `get_with_retry` function using unittest.mock.
    """

    @pytest.fixture(autouse=True)
    def septup(self):
        self.test_url = "http://example.com"

    @patch("app.utils.get_with_retry.requests.get")
    def test_successful_request(self, mock_get):
        """
        Test that a successful request returns.
        """
        expected_response = {"key": "value"}

        mock_response = MagicMock()
        mock_response.json.return_value = expected_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = get_with_retry(self.test_url)
        assert response == expected_response
        mock_get.assert_called_once_with(url=self.test_url, json=None, headers=None)

    @patch("app.utils.get_with_retry.requests.get")
    def test_retry_on_failure(self, mock_get):
        """
        Test that the function retries on failure and succeeds on a later attempt.
        """
        expected_response = {"key": "value"}

        mock_response_fail = MagicMock()
        mock_response_fail.raise_for_status.side_effect = HTTPError("Server Error")

        mock_response_success = MagicMock()
        mock_response_success.json.return_value = expected_response
        mock_response_success.status_code = 200

        mock_get.side_effect = [
            mock_response_fail,
            mock_response_fail,
            mock_response_success,
        ]

        response = get_with_retry(self.test_url)
        assert response == expected_response
        assert mock_get.call_count == 3
