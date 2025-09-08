import os

import boto3


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
        response = self.s3_client.put_object(
            Body=data, Key=key, Bucket=self.bucket_name, ContentType="application/json"
        )
        return response
