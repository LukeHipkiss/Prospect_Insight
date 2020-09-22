from insight_tool import settings
from insight_tool.utils import tribe_score


class LighthouseReport(dict):
    """A wrapper for LightHouse json reports.
    https://github.com/GoogleChrome/lighthouse
    """

    PERFORMANCE_WEIGHTS = settings.PERFORMANCE_WEIGHTS

    def __init__(self, *args, **kwargs):
        """Initialises the dictionary and sets at root:
        * metrics : A summary of general useful metrics for comparison.
        * performance_score: The overall report's score
        * performance_class: The overall report's class (Tribe metrics)
        """
        super(LighthouseReport, self).__init__(*args, **kwargs)
        self["performance_score"] = 0
        self["performance_class"] = ""
        self["metrics"] = {}

        self._transform_data()

    def __getattr__(self, name: str):
        """Return the values from a dictionary as if it were class attributes."""
        return self[name]

    def _transform_data(self):
        """Populates individual metrics parameters and define global scores."""

        performance_score = 0

        for perf_type, weight in self.PERFORMANCE_WEIGHTS.items():
            metric_score = self["audits"][perf_type]["score"]
            performance_score += metric_score * weight

            self["metrics"][perf_type] = {
                "score": metric_score,
                "timing": round(self["audits"][perf_type]["numericValue"], 0),
                "perf_class": tribe_score(metric_score * 100),
            }

        final_score = round(performance_score, 0)
        self["performance_score"] = final_score
        self["performance_class"] = tribe_score(final_score)

    def metric_score(self, metric_name):
        """Convenience method for retrieving the score for a particular metric."""
        assert metric_name in self.PERFORMANCE_WEIGHTS.keys()
        return self["metrics"][metric_name]["score"]

    def metric_timing(self, metric_name):
        """Convenience method for retrieving the timing for a particular metric."""
        assert metric_name in self.PERFORMANCE_WEIGHTS.keys()
        return self.data["metrics"][metric_name]["timing"]

    def metric_performance_class(self, metric_name):
        """Convenience method for retrieving the performance class for a particular metric."""
        assert metric_name in self.PERFORMANCE_WEIGHTS.keys()
        return self.data["metrics"][metric_name]["perf_class"]


if __name__ == "__main__":

    # Temp tests
    with open("test.json") as f:
        import json

        report = LighthouseReport(json.load(f))

    assert report.performance_score != 0
