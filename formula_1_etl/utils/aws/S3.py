import os

import boto3
from botocore.exceptions import ClientError


class S3UploadError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class S3:
    def __init__(self, bucket_name):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
            region_name=os.environ.get("REGION"),
        )
        self.bucket_name = bucket_name

    def upload_file(self, data, key):
        try:
            response = self.s3_client.put_object(
                Body=data,
                Key=key,
                Bucket=self.bucket_name,
                ContentType="application/json",
            )
            return response
        except ClientError as e:
            raise S3UploadError(
                e.response["Error"]["Message"],
                status_code=e.response["ResponseMetadata"]["HTTPStatusCode"],
            ) from e
