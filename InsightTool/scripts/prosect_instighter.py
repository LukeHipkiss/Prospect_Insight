import json
from pprint import pprint
from os import path
from ProspectInstights.config import root_dir
from ProspectInstights.InsightTool.scripts.lighthouse import LighthouseRunner
from ProspectInstights.InsightTool.scripts.lighthouse import LighthouseReport

PROPOSAL_URL = "https://www.google.com/"
COMPETITOR_URL_1 = "https://duckduckgo.com/"
COMPETITOR_URL_2 = "https://www.bing.com/"

URL_LIST = [PROPOSAL_URL, COMPETITOR_URL_1, COMPETITOR_URL_2]

PATH_TO_TEST_FOLDER = str(root_dir()) + "/InsightTool/tests/"

DEBUG = False


def report_exists(file_path):
    return path.exists(file_path)


def save_report(report: json, name: str, overwrite=False):
    target_path = PATH_TO_TEST_FOLDER + name.replace('/', '_') + '.json'

    if not overwrite and report_exists(target_path):
        return

    with open(target_path, 'w') as report_to_save:
        json.dump(report, report_to_save)


def load_report(name: str):
    with open(PATH_TO_TEST_FOLDER + name.replace('/', '_') + '.json', 'r') as report_to_load:
        return json.load(report_to_load)


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
        reports = [LighthouseRunner(url).report for url in URL_LIST]

    for report in reports:

        if DEBUG:
            save_report(report, report.url)

        print(report.url, report.overall_performance_score)


if __name__ == '__main__':
    main()
