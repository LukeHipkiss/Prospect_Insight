import unittest
import json
from ProspectInstights.config import root_dir
from ProspectInstights.InsightTool.scripts.lighthouse.report import LighthouseReport

TEST_JSON_FILE = str(root_dir()) + "/InsightTool/tests/test_response.json"
EXPECTED_DATA = {
    'fetch_time': '2020-09-16T13:03:29.810Z',
    'URL': 'https://shop.polymer-project.org/',
    'metrics': {
        'first-contentful-paint': {'score': 0.65, 'timing': 1357.0, 'perf_class': 'orange'},
        'speed-index': {'score': 0.21, 'timing': 3278, 'perf_class': 'red'},
        'largest-contentful-paint': {'score': 0.11, 'timing': 4658.0, 'perf_class': 'red'},
        'interactive': {'score': 0.49, 'timing': 4527.0, 'perf_class': 'red'},
        'total-blocking-time': {'score': 0.39, 'timing': 423.0, 'perf_class': 'red'},
        'cumulative-layout-shift': {'score': 1, 'timing': 0, 'perf_class': 'green'}
    },
    'performance_score': 38.0,
    'performance_class': 'red'
}


class MyTestCase(unittest.TestCase):

    def test_lighthouse_report(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        self.assertDictEqual(
            report.filtered_data,
            EXPECTED_DATA,
        )

    def test_url(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        self.assertEqual(
            report.url,
            EXPECTED_DATA["URL"]
        )

    def test_fetch_time(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        self.assertEqual(
            report.fetch_time,
            EXPECTED_DATA["fetch_time"]
        )

    def test_metric_keys(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        self.assertEqual(
            report.metric_keys,
            EXPECTED_DATA["metrics"].keys()
        )

    def test_metrics(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        self.assertEqual(
            report.metrics,
            EXPECTED_DATA["metrics"]
        )

    def test_correct_metric_name_score(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        for metric_name in report.metric_keys:
            self.assertEqual(
                report.score(metric_name),
                EXPECTED_DATA["metrics"][metric_name]["score"]
            )

    def test_incorrect_metric_name_score(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        self.assertEqual(
            report.score("blah"),
            "Given timing was not found"
        )

    def test_correct_metric_name_timing(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        for metric_name in report.metric_keys:
            self.assertEqual(
                report.timing(metric_name),
                EXPECTED_DATA["metrics"][metric_name]["timing"]
            )

    def test_incorrect_metric_name_timing(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        self.assertEqual(
            report.timing("blah"),
            "Given timing was not found"
        )

    def test_correct_metric_name_perf_class(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        for metric_name in report.metric_keys:
            self.assertEqual(
                report.metric_performance_class(metric_name),
                EXPECTED_DATA["metrics"][metric_name]["perf_class"]
            )

    def test_incorrect_metric_name_perf_class(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        self.assertEqual(
            report.metric_performance_class("blah"),
            "Given timing was not found"
        )

    def test_overall_performance_class(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        self.assertEqual(
            report.overall_performance_class,
            EXPECTED_DATA["performance_class"]
        )

    def test_overall_performance_score(self):

        with open(TEST_JSON_FILE, 'r') as fil:
            report = LighthouseReport(json.load(fil))

        self.assertEqual(
            report.overall_performance_score,
            EXPECTED_DATA["performance_score"]
        )


if __name__ == '__main__':
    unittest.main()
