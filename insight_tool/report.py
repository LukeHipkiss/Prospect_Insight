# Material for a settings.py ???
PERFORMANCE_TIMINGS = [
    ('first-contentful-paint', 15),
    ('speed-index', 15),
    ('largest-contentful-paint', 25),
    ('interactive', 15),
    ('total-blocking-time', 25),
    ('cumulative-layout-shift', 5),
]

# WHat the heck is this?
"""list(str) default list of timings"""


# It seems to me that it would be more fitting for this class to inherit from dict
class LighthouseReport(object):
    # from_load is never used? If you don't need it yet don't add it :P
    def __init__(self, data, from_load=False):
        """
        Args:
            data (dict): JSON loaded lighthouse report
        """
        # Man stop using dunder attributes you will have yourself in no time :D
        self.__timings = PERFORMANCE_TIMINGS
        # NOTE: Should we save the original report somewhere for safe keeping? - Not lucas here....

        self.data = self.filter_data(data) if not from_load else data

    def filter_data(self, data):
        # NOTE: May be good to have a unique ID to link prospect with competitors - Not lucas here...

        performance_score = 0

        filtered_data = {
            "fetch_time": data["fetchTime"],
            "URL": data["finalUrl"],
            "metrics": {}
        }
        # This seems to be at the core of the project. I think it shouldn't live in Report
        # It's more like the score engine, you need to explain and test well your objectives here.
        # I won't try to get it from here, I'd rather you explain it to me in person.
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


    # Part of what I mentioned above, this is not report this is engine.
    @staticmethod
    def __get_score_class(score):
        score_class = "red"

        if score > 49:
            score_class = "orange" if score < 90 else "green"

        return score_class



    # rather than having a bunch of properties, if you inherit from dict you can add the attributes
    # Below an example of something I implemented the other day.
    # it would need a special check for metric_keys, but I'm not sure you need metric_keys anyway...
    #
    # def __getattr__(self, name: str):
    #     """ Return the values from a dictionary as if it were class attributes.
    #     """
    #
    #     return self[name]

    @property
    def metric_keys(self):
        return self.data["metrics"].keys()

    @property
    def metrics(self):
        return self.data["metrics"]

    @property
    def url(self):
        return self.data["URL"]

    @property
    def fetch_time(self):
        return self.data["fetch_time"]

    @property
    def overall_performance_class(self):
        return self.data["performance_class"]

    @property
    def overall_performance_score(self):
        return self.data["performance_score"]



    # It seems to be that we need to talk about these methods...
    # As I'm suspecting that you altering the main raw data to add the results of the engine calculations
    # If that's the case we need to think carefully about that, maybe a different json? We could use this smaller json
    # as quick view or would that be more likely what we would want to preserve in the long term, etc...
    def score(self, metric_name):
        try:
            return self.data["metrics"][metric_name]["score"]

        except KeyError:
            return "Given timing was not found"

    def timing(self, metric_name):
        try:
            return self.data["metrics"][metric_name]["timing"]

        except KeyError:
            return "Given timing was not found"

    def metric_performance_class(self, metric_name):
        try:
            return self.data["metrics"][metric_name]["perf_class"]

        except KeyError:
            return "Given timing was not found"

# Finally, make sure you add docstrings where due and document your intentions throughout! :D
