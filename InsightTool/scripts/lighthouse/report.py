# this python file uses the following encoding utf-8

# Python Standard Library

PERFORMANCE_TIMINGS = [
    ('first-contentful-paint', 15),
    ('speed-index', 15),
    ('largest-contentful-paint', 25),
    ('interactive', 15),
    ('total-blocking-time', 25),
    ('cumulative-layout-shift', 5),
]
"""list(str) default list of timings"""


class LighthouseReport(object):

    def __init__(self, data):
        """
        Args:
            data (dict): JSON loaded lighthouse report
        """
        self.__timings = PERFORMANCE_TIMINGS
        # NOTE: Should we save the original report somewhere for safe keeping?

        self.filtered_data = self.filter_data(data)

    def filter_data(self, data):
        # NOTE: May be good to have a unique ID to link prospect with competitors

        performance_score = 0

        filtered_data = {
            "fetch_time": data["fetchTime"],
            "URL": data["finalUrl"],
            "metrics": {}
        }

        for timing, weight in self.__timings:
            metric_score = data["audits"][timing]["score"]
            performance_score += (metric_score * weight)

            filtered_data["metrics"][timing] = {
                "score": metric_score,
                "timing": round(data["audits"][timing]["numericValue"], 0),
                "perf_class": self.__get_score_class(metric_score * 100)
            }

        filtered_data["performance_score"] = round(performance_score, 0)
        filtered_data["performance_class"] = self.__get_score_class(round(performance_score, 0))

        return filtered_data

    @staticmethod
    def __get_score_class(score):
        score_class = "red"

        if score > 49:
            score_class = "orange" if score < 90 else "green"

        return score_class

    @property
    def metric_keys(self):
        return self.filtered_data["metrics"].keys()

    @property
    def metrics(self):
        return self.filtered_data["metrics"]

    @property
    def url(self):
        return self.filtered_data["URL"]

    @property
    def fetch_time(self):
        return self.filtered_data["fetch_time"]

    @property
    def overall_performance_class(self):
        return self.filtered_data["performance_class"]

    @property
    def overall_performance_score(self):
        return self.filtered_data["performance_score"]

    def score(self, metric_name):
        try:
            return self.filtered_data["metrics"][metric_name]["score"]

        except KeyError:
            return "Given timing was not found"

    def timing(self, metric_name):
        try:
            return self.filtered_data["metrics"][metric_name]["timing"]

        except KeyError:
            return "Given timing was not found"

    def metric_performance_class(self, metric_name):
        try:
            return self.filtered_data["metrics"][metric_name]["perf_class"]

        except KeyError:
            return "Given timing was not found"
