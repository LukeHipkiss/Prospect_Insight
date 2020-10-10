import os
import sys
import subprocess

import boto3
from botocore.client import Config


s3 = boto3.resource('s3',
                    endpoint_url='http://minio:9000',
                    aws_access_key_id='AKIAIOSFODNN7EXAMPLE',
                    aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

MAIN = "lighthouse"
REPORTS_PATH = "/home/chrome/reports/"


def light_worker(
    url,
    file_name,
    prospect,
    emulated_form_factor="desktop",
    chrome_flags="--headless --disable-gpu --no-sandbox",
    preset="perf",
    output="json,html",
):
    """Wraps around lighthouse-cli.
    https://github.com/GoogleChrome/lighthouse#cli-options
    """
    assert emulated_form_factor in ["mobile", "desktop"]

    file_path = REPORTS_PATH + file_name

    command = [
        MAIN,
        url,
        f"--chrome-flags={chrome_flags}",
        f"--preset={preset}",
        f"--emulated-form-factor={emulated_form_factor}",
        f"--output={output}",
        f"--output-path={file_path}",
    ]

    process = subprocess.run(command, stdout=sys.stdout, stderr=subprocess.STDOUT)

    if process.returncode == 0:
        bucket = s3.Bucket(prospect)
        if not bucket.creation_date:
            bucket = s3.create_bucket(Bucket=prospect)

        bucket.upload_file(f"{file_path}.report.json", f"{file_name}.report.json")

        os.remove(f"{file_path}.report.json")

    return process.returncode


if __name__ == "__main__":

    r = light_worker("https://www.google.com", "abc123", "fitflop")
