import json

from formula_1_etl.utils.aws.S3 import S3
from formula_1_etl.utils.create_name_files import create_root_path
from formula_1_etl.utils.get_api import RequestError
from formula_1_etl.utils.handle_request import handle_requests


def lambda_handler(event, context):
    try:
        endpoint = event.get("endpoint")
        bucket_name = event.get("bucket_name")
        layer_name = event.get("layer_name")

        key = create_root_path(layer_name=layer_name, endpoint=endpoint)

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
