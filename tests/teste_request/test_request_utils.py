from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import HTTPError, RequestException, Timeout

from formula_1_etl.utils.get_api import RequestError, request_url

offset = 0
limit = 100

params = {"offset": offset, "limit": limit}


@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_status_200_request_api(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {
        "Server": "nginx/1.28.0",
        "Date": "Fri, 05 Sep 2025 16:16:59 GMT",
        "Content-Type": "application/json",
        "Transfer-Encoding": "chunked",
        "Connection": "keep-alive",
        "Vary": "Accept, origin",
        "Allow": "GET, HEAD, OPTIONS",
        "Expires": "Fri, 05 Sep 2025 16:30:04 GMT",
        "Cache-Control": "max-age=3600",
        "Age": "2815",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "same-origin",
        "Cross-Origin-Opener-Policy": "same-origin",
        "Content-Encoding": "gzip",
    }

    mock_get.return_value = mock_response
    endpoint = "2025/races"
    response = request_url(endpoint=endpoint, params=params)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


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
        request_url(endpoint=endpoint, params=params)

    e = excinfo.value
    assert e.status_code == 404
    assert "The requested resource was not found on this server" in e.response_body
    assert e.endpoint == endpoint


@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_erro_timeout(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Timeout(response=mock_response)
    mock_get.return_value = mock_response
    endpoint = "2025/races"
    with pytest.raises(RequestError) as excinfo:
        request_url(endpoint=endpoint, params=params)

    e = excinfo.value
    assert e.status_code is None
    assert "Erro Devido a Timeout" == e.response_body
    assert e.endpoint == endpoint


@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_erro_generico(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = RequestException(
        response=mock_response
    )
    mock_get.return_value = mock_response
    endpoint = "2025/races"
    with pytest.raises(RequestError) as excinfo:
        request_url(endpoint=endpoint, params=params)

    e = excinfo.value
    assert e.status_code is None
    assert "Erro Generico Request" == e.response_body
    assert e.endpoint == endpoint
