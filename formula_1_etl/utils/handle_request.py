from formula_1_etl.utils.get_api import request_url


def handle_requests(endpoint, limit=100):
    total = float("inf")
    offset = 0

    params = {"offset": offset, "limit": limit}

    data = []

    while offset < total:
        response = request_url(endpoint=endpoint, params=params).json()
        data.append(response)
        total = int(response["MRData"]["total"])
        offset += limit
        params["offset"] = offset

    return data
