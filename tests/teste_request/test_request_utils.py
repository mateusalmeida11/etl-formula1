from formula_1_etl.utils.get_api import get_request


def test_status_200_request_api():
    url = "https://api.jolpi.ca/ergast/f1/2025/races"
    response = get_request(url=url)
    assert response.status_code == 200
