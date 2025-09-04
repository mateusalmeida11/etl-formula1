from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import HTTPError, Timeout

from formula_1_etl.utils.get_api import RequestError, request_url


@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_status_200_request_api(mock_get):
    mock_get.return_value.status_code = 200
    endpoint = "2025/races"
    response = request_url(endpoint=endpoint)
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
    endpoint = "2025321/races"
    with pytest.raises(RequestError) as excinfo:
        request_url(endpoint=endpoint)

    e = excinfo.value
    assert e.status_code == 404
    assert "The requested resource was not found on this server" in e.response_body
    assert e.endpoint == endpoint


@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_erro_timeout(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Timeout
    mock_get.return_value = mock_response
    endpoint = "2025321/races"
    with pytest.raises(Timeout) as excinfo:
        request_url(endpoint=endpoint)

    e = excinfo.value
    assert e.status_code is None
    assert "Erro Devido a Timeout" in e.response_body
    assert e.endpoint == endpoint
