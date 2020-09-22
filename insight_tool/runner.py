import json
import os
import subprocess
import tempfile

from report import LighthouseReport


class LighthouseRunner(object):
    """
    Lightweight runner, wraps around lighthouse-cli and parses the result

    Attributes:
        report (LighthouseReport): object with simplified report
    """

    def __init__(
        self,
        url,
        form_factor="desktop",
        quiet=True,
        additional_settings=None,
        debug=False,
    ):
        """
        Args:
            url (str): url to test
            form_factor (str, optional): either mobile or desktop,
                default is mobile
            quiet (bool, optional): should not output anything to stdout,
                default is True
            additional_settings (list, optional): list of additional params
        """

        # I wouldn't make it dunder here, as it's harder to test.
        self.__debug = debug

        assert form_factor in ["mobile", "desktop"]

        # Avoid logic in the init, it's harder to debug and can make things confusing
        # Maybe it could make sense to have a __call__ method but as a first stance, move this action to a method that
        # you will explicitly call.
        if not self.__debug:
            _, self.__report_path = tempfile.mkstemp(suffix=".json")
            self._run(url, form_factor, quiet, additional_settings)

        else:
            # Right, this is indicating that you are confusing debug with testing.
            # Usually when you add "debug" to the main code it means you will output more information about what's
            # going on, not that you will run a test.
            # My advice here is make the interface flexible enough so that it's easy for you to test, but keep things
            # separate, moving the logic out of the init is a start.
            self.__report_path = "sample_response.json"

        self.report = self._get_report()
        self._clean()

    # Same point again, call this explicitly no need to be a private method.
    # All of these parameters can be defined as instance attributes.
    def _run(self, url, form_factor, quiet, additional_settings=None):
        # why? :P
        report_path = self.__report_path

        # This will only have value if you document, if you don't need it now then YAGNI... (When you need the flexibility you add it
        # keep complexity to a minimum
        additional_settings = additional_settings or []

        try:
            # this is too important to be hidden here like that, for the main command you could define a class variable.
            # maybe the flags needed could be init args if they are prone to change, or at least parameters.
            command = [
                "lighthouse",
                url,
                "--quiet" if quiet else "",
                '--chrome-flags="--headless"',
                "--preset=perf",
                "--emulated-form-factor={0}".format(form_factor),
                "--output=json",
                "--output-path={0}".format(report_path),
            ]

            command = command + additional_settings
            subprocess.check_call(" ".join(command), shell=True)
        except subprocess.CalledProcessError as exc:
            # What's the benefit of this? I'd personally just not catch it
            # What are the conditions that this fails?
            msg = """
                Command "{0}"
                returned an error code: {1},
                output: {2}
            """.format(
                exc.cmd, exc.returncode, exc.output
            )
            raise RuntimeError(msg)

    # Not sure if it's applicable as I haven't used lighthouse yet, but if the result of calling the command is the json output
    # then you might as well not define a place to save or add quiet, that way you could have the report in memory, and only save
    # if you wish, opening a file is less desirable particularly if you want to clean it after...
    # Generally keeping things in memory and being mindful about IO is a good idea... (Not really a concern here too much)
    def _get_report(self):
        with open(self.__report_path, "r") as fil:
            return LighthouseReport(json.load(fil))

    def _clean(self):
        # No need to have a debug here, just call the clean where it is needed... within the conditional
        if self.__debug:
            return

        os.remove(self.__report_path)
