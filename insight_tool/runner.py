import subprocess

from insight_tool import settings


class LighthouseRunner:
    """Lightweight runner, wraps around lighthouse-cli.
    https://github.com/GoogleChrome/lighthouse#cli-options
    """

    MAIN = "lighthouse"

    def __init__(
        self,
        url,
        file_name,
        emulated_form_factor="desktop",
        chrome_flags="--headless",
        preset="perf",
        output="json",
    ):
        """ Parameters matches the cli, saving as a json is implied.
        """
        assert emulated_form_factor in ["mobile", "desktop"]

        self.command = [
            self.MAIN,
            url,
            f"--chrome-flags={chrome_flags}",
            f"--preset={preset}",
            f"--emulated-form-factor={emulated_form_factor}",
            f"--output={output}",
            f"--output-path={settings.REPORT_PATH + file_name}",
        ]

    def run(self):
        """Executes lighthouse within a subshell and returns the exit code"""
        process = subprocess.run(self.command)
        return process.returncode

    def __call__(self):
        """Convenience call to simplify interface"""
        return self.run()


if __name__ == "__main__":
    # Just a simple test prior to proper unit testing it.
    LighthouseRunner("https://www.google.com", "test.json")()
