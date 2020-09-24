import os
import sys
import subprocess

import click


class LighthouseRunner:
    """Lightweight runner, wraps around lighthouse-cli.
    https://github.com/GoogleChrome/lighthouse#cli-options
    """

    MAIN = "lighthouse"

    def __init__(
        self,
        url,
        file_path,
        emulated_form_factor="desktop",
        chrome_flags="--headless --disable-gpu --no-sandbox",
        preset="perf",
        output="json",
    ):
        """Parameters matches the cli, saving as a json is implied."""
        assert emulated_form_factor in ["mobile", "desktop"]

        self.command = [
            self.MAIN,
            url,
            f"--chrome-flags={chrome_flags}",
            f"--preset={preset}",
            f"--emulated-form-factor={emulated_form_factor}",
            f"--output={output}",
            f"--output-path={os.path.join(file_path)}",
        ]

    def run(self):
        """Executes lighthouse within a subshell and returns the exit code"""
        process = subprocess.run(
            self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(f"Process completed with exit status:{process.returncode}")
        return process.returncode

    def __call__(self):
        """Convenience call to simplify interface"""
        return self.run()


@click.command()
@click.argument("url")
@click.argument("path")
def main(url, path):
    """Entrypoint for the lighthouse runner, it requires two arguments in order:
    * An url to be tested.
    * A file path where the report will be saved.
    """
    return_code = LighthouseRunner(url, path)()
    sys.exit(return_code)
