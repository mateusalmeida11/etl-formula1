import json

import boto3
from moto import mock_aws

from formula_1_etl.utils.aws.S3 import S3


@mock_aws
def test_upload_s3_success():
    bucket_name = "etl-formula-1"

    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket=bucket_name)

    key = "raw/seasons/2025/09/01/all_seasons.json"
    body = {
        "MRData": {
            "xmlns": "",
            "series": "f1",
            "url": "https://api.jolpi.ca/ergast/f1/seasons/",
            "limit": "30",
            "offset": "0",
            "total": "76",
            "SeasonTable": {
                "Seasons": [
                    {
                        "season": "1950",
                        "url": "https://en.wikipedia.org/wiki/1950_Formula_One_season",
                    }
                ]
            },
        }
    }
    json_data = json.dumps(body, indent=4)
    s3 = S3(bucket_name=bucket_name)
    response = s3.upload_file(data=json_data, key=key)

    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    assert status_code == 200
    assert "ETag" in response


@mock_aws
def test_upload_s3_bucket_inexistente():
    bucket_name = "etl-formula-1"

    boto3.client("s3", region_name="us-east-1")

    key = "raw/seasons/2025/09/01/all_seasons.json"
    body = {
        "MRData": {
            "xmlns": "",
            "series": "f1",
            "url": "https://api.jolpi.ca/ergast/f1/seasons/",
            "limit": "30",
            "offset": "0",
            "total": "76",
            "SeasonTable": {
                "Seasons": [
                    {
                        "season": "1950",
                        "url": "https://en.wikipedia.org/wiki/1950_Formula_One_season",
                    }
                ]
            },
        }
    }
    json_data = json.dumps(body, indent=4)
    s3 = S3(bucket_name=bucket_name)
    response = s3.upload_file(data=json_data, key=key)

    error = response.response
    status_code = error["HTTPStatusCode"]
    assert status_code == 404
