from unittest.mock import MagicMock, patch

import boto3
from moto import mock_aws
from requests.exceptions import HTTPError

from formula_1_etl.layers.layer_raw.handler_request_api import lambda_handler


@mock_aws
@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_success_upload_s3_bucket_process_complete(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "MRData": {
            "xmlns": "",
            "series": "f1",
            "url": "https://api.jolpi.ca/ergast/f1/2025/races/",
            "offset": "0",
            "total": "1",
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

    bucket_name = "etl-formula-1"
    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket=bucket_name)

    event = {
        "category": "races",
        "bucket_name": bucket_name,
        "layer_name": "raw",
        "season": 2025,
    }
    context = {}

    result = lambda_handler(event=event, context=context)
    assert result["status"] == "success"
    assert result["bucket"] == bucket_name
    assert result["s3_response"]["status_code"] == 200


@mock_aws
@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_fail_request_error_raw(mock_get):
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

    bucket_name = "etl-formula-1"
    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket=bucket_name)

    event = {
        "category": "races",
        "bucket_name": bucket_name,
        "layer_name": "raw",
        "season": 2025,
    }
    context = {}

    response = lambda_handler(event=event, context=context)

    assert response["status"] == "error"
    assert response["type"] == "APIError"
    assert response["status_code"] == 404
    assert response["endpoint"] == "2025/races"


@mock_aws
@patch("formula_1_etl.utils.get_api.requests.Session.get")
def test_fail_upload_s3(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "MRData": {
            "xmlns": "",
            "series": "f1",
            "url": "https://api.jolpi.ca/ergast/f1/2025/races/",
            "offset": "0",
            "total": "1",
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

    bucket_name = "etl-formula-1"
    boto3.client("s3", region_name="us-east-1")

    event = {
        "category": "races",
        "bucket_name": bucket_name,
        "layer_name": "raw",
        "season": 2025,
    }
    context = {}
    response = lambda_handler(event=event, context=context)

    assert response["status"] == "error"
    assert response["type"] == "S3UploadError"
    assert response["status_code"] == 404
    assert response["bucket"] == bucket_name
