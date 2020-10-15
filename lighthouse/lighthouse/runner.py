import os
import sys
import subprocess
import logging

from lighthouse.s3 import get_or_create_bucket

logger = logging.getLogger(__name__)

MAIN = "lighthouse"
REPORTS_PATH = "/home/chrome/reports/"


def light_worker(
    url,
    tag,
    _type,
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

    file_path = REPORTS_PATH + f"{tag}-{_type}"

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

        try:
            # We should break this dependency by having a different service upload the file, not urgent though...
            bucket = get_or_create_bucket(prospect)
            bucket.upload_file(f"{file_path}.report.json", f"{tag}/{_type}.report.json")
        except Exception:
            logger.exception("Failed to upload report to s3")

        os.remove(f"{file_path}.report.json")

    return process.returncode


if __name__ == "__main__":

    light_worker("https://www.google.com", "abc123", "main", "fitflop")
