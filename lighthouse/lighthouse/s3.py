import os

import boto3
from botocore.client import Config


s3 = boto3.resource(
    "s3",
    endpoint_url=os.environ.get("MINIO_URL"),
    aws_access_key_id=os.environ.get("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("MINIO_SECRET_KEY"),
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)


def sanitise(name: str) -> str:
    return "".join([c for c in name if c.islower()])


def get_or_create_bucket(name: str):

    name = sanitise(name)

    bucket = s3.Bucket(name)
    if not bucket.creation_date:
        bucket = s3.create_bucket(Bucket=name)

    return bucket
