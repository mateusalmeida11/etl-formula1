from unittest.mock import patch

from formula_1_etl.utils.get_api import request_url


@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_status_200_request_api(mock_get):
    mock_get.return_value.status_code = 200
    url = "https://api.jolpi.ca/ergast/f1/2025/races"
    response = request_url(url=url)
    assert response.status_code == 200
