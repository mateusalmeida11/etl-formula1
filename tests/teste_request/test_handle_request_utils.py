from unittest.mock import MagicMock, patch

from formula_1_etl.utils.handle_request import handle_requests


@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_retorno_da_lista_maior_que_zero(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "MRData": {
            "xmlns": "",
            "series": "f1",
            "url": "https://api.jolpi.ca/ergast/f1/2025/races/",
            "limit": "30",
            "offset": "0",
            "total": "24",
            "RaceTable": {
                "season": "2025",
                "Races": [
                    {
                        "season": "2025",
                        "round": "1",
                        "url": "https://en.wikipedia.org/wiki/2025_Australian_Grand_Prix",
                        "raceName": "Australian Grand Prix",
                    }
                ],
            },
        }
    }
    mock_get.return_value = mock_response
    endpoint = "/seasons"
    data = handle_requests(endpoint=endpoint)
    assert len(data) > 0
