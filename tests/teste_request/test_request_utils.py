from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import HTTPError

from formula_1_etl.utils.get_api import request_url


@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_status_200_request_api(mock_get):
    mock_get.return_value.status_code = 200
    url = "https://api.jolpi.ca/ergast/f1/2025/races"
    response = request_url(url=url)
    assert response.status_code == 200


@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_status_404_error_rout_endpoint(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = """
    <!doctype html>
    <html lang="en">
    <head>
      <title>Not Found</title>
    </head>
    <body>
      <h1>Not Found</h1><p>The requested resource was not found on this server.</p>
    </body>
    </html>
    """
    mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
    mock_get.return_value = mock_response
    url = "https://api.jolpi.ca123/ergast/f1/2025/races"
    with pytest.raises(HTTPError) as excinfo:
        request_url(url=url)

    e = excinfo.value
    assert e.response.status_code == 404
