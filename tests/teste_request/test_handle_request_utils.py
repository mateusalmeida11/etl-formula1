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


@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_logica_paginacao(mock_get):
    # página 1
    response_page1 = MagicMock()
    response_page1.status_code = 200
    response_page1.json.return_value = {
        "MRData": {
            "limit": "2",
            "offset": "0",
            "total": "5",
            "SeasonTable": {"Seasons": [{"season": "1950"}, {"season": "1951"}]},
        }
    }

    # página 2
    response_page2 = MagicMock()
    response_page2.status_code = 200
    response_page2.json.return_value = {
        "MRData": {
            "limit": "2",
            "offset": "2",
            "total": "5",
            "SeasonTable": {"Seasons": [{"season": "1952"}, {"season": "1953"}]},
        }
    }

    # página 3
    response_page3 = MagicMock()
    response_page3.status_code = 200
    response_page3.json.return_value = {
        "MRData": {
            "limit": "2",
            "offset": "4",
            "total": "5",
            "SeasonTable": {"Seasons": [{"season": "1954"}]},
        }
    }

    # side_effect = retorna cada mock em sequência
    mock_get.side_effect = [response_page1, response_page2, response_page3]
    endpoint = "/seasons"
    data = handle_requests(endpoint=endpoint, limit=2)
    page1 = data[0]["MRData"]["SeasonTable"]["Seasons"]
    assert len(data) == 3
    assert len(page1) == 2
