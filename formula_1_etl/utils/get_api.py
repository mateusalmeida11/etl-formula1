import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RequestError(Exception):
    def __init__(self, message, status_code=None, endpoint=None, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.endpoint = endpoint
        self.response_body = response_body


def request_url(endpoint):
    retry_strategy = Retry(
        total=3,
        status_forcelist=[408, 429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        backoff_factor=1,
    )
    url = "https://api.jolpi.ca/ergast/f1/"
    url += endpoint
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    try:
        response = http.get(url=url)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        raise RequestError(
            f"HTTP Error {e.response.status_code}",
            status_code=e.response.status_code,
            endpoint=endpoint,
            response_body=e.response.text,
        ) from e
    except requests.exceptions.Timeout as e:
        raise RequestError(
            "Erro Timeout", endpoint=endpoint, response_body="Erro Devido a Timeout"
        ) from e
    except requests.exceptions.RequestException as e:
        raise RequestError(
            "Erro Generico Request",
            endpoint=endpoint,
            response_body="Erro Generico Request",
        ) from e
