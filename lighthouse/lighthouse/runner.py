import sys
import subprocess

MAIN = "lighthouse"
REPORTS_PATH = "/home/chrome/reports/"


def light_worker(
    url,
    tag,
    type,
    emulated_form_factor="desktop",
    chrome_flags="--headless --disable-gpu --no-sandbox",
    preset="perf",
    output="json",
):
    """ Wraps around lighthouse-cli.
    https://github.com/GoogleChrome/lighthouse#cli-options
    """
    assert emulated_form_factor in ["mobile", "desktop"]

    file_path = REPORTS_PATH + f"{tag}-{type}.json"

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

    return process.returncode


if __name__ == '__main__':

    r = light_worker("https://www.google.com", "abc123", "test")
