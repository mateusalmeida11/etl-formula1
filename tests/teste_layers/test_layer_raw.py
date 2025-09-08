from unittest.mock import MagicMock, patch

import boto3
from moto import mock_aws

from formula_1_etl.layers.layer_raw import lambda_handler


@mock_aws
@patch("fomrula_1_etl.utils.get_api.requests.Session.get")
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
    event = {"endpoint": "2025/races"}
    context = {}

    bucket_name = "etl-formula-1"
    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket=bucket_name)

    result = lambda_handler(event=event, context=context)
    assert result["status"] == "success"
