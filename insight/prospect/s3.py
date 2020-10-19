import os
import json

import boto3
from botocore.client import Config

from prospect.report import LighthouseReport


s3 = boto3.resource(
    "s3",
    endpoint_url=os.environ.get("MINIO_URL"),
    aws_access_key_id=os.environ.get("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("MINIO_SECRET_KEY"),
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)


def get_json_reports(report):

    reports = []
    for i in ["main", "comp1", "comp2"]:

        content_object = s3.Object(report.prospect.name, f"{report.tag}/{i}.report.json")
        file_content = content_object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)

        reports.append(LighthouseReport(json_content))

    return reports
