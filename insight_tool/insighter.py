import json
from os import path  # Best only importing os for readability (It helps to know where it's coming from)

from runner import LighthouseRunner
from report import LighthouseReport


# Bunch of settings to go on a general settings.py

PROPOSAL_URL = "https://www.google.com/"
COMPETITOR_URL_1 = "https://duckduckgo.com/"
COMPETITOR_URL_2 = "https://www.bing.com/"

URL_LIST = [PROPOSAL_URL, COMPETITOR_URL_1, COMPETITOR_URL_2]

PATH_TO_TEST_FOLDER = "tests/"

DEBUG = True


# Too simple to abstract
def report_exists(file_path):
    return path.exists(file_path)


# That should be a more general function, if you want a more specialised behaviour then change the name and add a docstring
# Bear in mind that you are already passing the object so if you always want to save based on the url you can handle that internally
# rather than having the second redundant parameter.  This overwrite is likely to cause bugs, I'd simplify things there...
# You should take the target path as input.
def save_report(report: json, name: str, overwrite=False):
    target_path = PATH_TO_TEST_FOLDER + name.replace('/', '_') + '.json'

    if not overwrite and report_exists(target_path):
        return

    with open(target_path, 'w') as report_to_save:
        json.dump(report, report_to_save)


# This is starting to look like a class, perhaps a class Report? with the save and load abstracted away among everything else.
def load_report(name: str):
    with open(PATH_TO_TEST_FOLDER + name.replace('/', '_') + '.json', 'r') as report_to_load:
        return json.load(report_to_load)

# We should take things as input, even if we have some defaults, "click" for the rescue!
def main():

    if DEBUG:


        reports_to_run = [
            url
            for url in URL_LIST
            if not report_exists(PATH_TO_TEST_FOLDER + url.replace('/', '_') + '.json')
        ]
        reports_to_load = list(set(URL_LIST).difference(set(reports_to_run)))

        reports_to_run = [LighthouseRunner(url).report for url in reports_to_run]
        reports_to_load = [LighthouseReport(load_report(url), from_load=True) for url in reports_to_load]

        reports = reports_to_run + reports_to_load

    else:
        # This interface is not very friendly, I haven't looked yet at the Runner, but can't we feed the list instead?
        # Also just for the sake of keeping things clear and making debugging easier as well, declare the class,
        # probably instead of doing all the "magic" during instantiation, call a method to run things and then get an
        # output, trust me once a bug crops up this will make your life 1000 times easier.
        reports = [LighthouseRunner(url).report for url in URL_LIST]

    for report in reports:

        # I don't think we need to check debug twice, just do it within the scope of debug above...
        # Wait you only save if debugging? otherwise you print? That's confusing... What's going on?
        # What should this module really do? Maybe it won't have a purpose once the web app is in place?
        if DEBUG:
            save_report(report, report.url)
        # should this be here? it's looking like debug code, if you want logging, import logging :P
        print(report.url, report.overall_performance_score)


if __name__ == '__main__':
    main()
