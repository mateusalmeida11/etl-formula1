import json

from formula_1_etl.utils.aws.S3 import S3, S3UploadError
from formula_1_etl.utils.build_endpoint import build_endpoint
from formula_1_etl.utils.create_name_files import create_root_path
from formula_1_etl.utils.get_api import RequestError
from formula_1_etl.utils.handle_request import handle_requests


def lambda_handler(event, context):
    try:
        category = event.get("category")
        season = event.get("season")
        rounds = event.get("rounds")
        bucket_name = event.get("bucket_name")
        layer_name = event.get("layer_name")

        key = create_root_path(layer_name=layer_name, category=category)
        endpoint = build_endpoint(category=category, season=season, rounds=rounds)

        data = handle_requests(endpoint=endpoint)

        json_data = json.dumps(data, indent=4)
        s3 = S3(bucket_name=bucket_name)
        response = s3.upload_file(data=json_data, key=key)
        return {
            "status": "success",
            "bucket": bucket_name,
            "key": key,
            "total_pages": len(data),
            "s3_response": {
                "status_code": response["ResponseMetadata"]["HTTPStatusCode"]
            },
        }
    except RequestError as e:
        return {
            "status": "error",
            "type": "APIError",
            "status_code": e.status_code or 500,
            "message": str(e),
            "endpoint": endpoint,
        }
    except S3UploadError as e:
        return {
            "status": "error",
            "type": "S3UploadError",
            "status_code": e.status_code,
            "message": str(e.message),
            "bucket": bucket_name,
            "key": key,
        }
