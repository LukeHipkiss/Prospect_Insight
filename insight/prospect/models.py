from django.db import models


class Prospect(models.Model):
    name = models.CharField(max_length=200, unique=True)
    reports = models.IntegerField(default=0)
    last = models.DateTimeField(auto_now=True)
    last_tag = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @classmethod
    def update_last_report(cls, name, tag):
        """Update the prospect row's number of reports and last time generated
        The timestamp is updated every time the row is touched
        """

        prospect = cls.objects.get(name=name)
        prospect.reports += 1
        prospect.last_tag = tag
        prospect.save()


class Report(models.Model):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=200)

    def __str__(self):
        return f"Report for {self.prospect}, using url: {self.url} generated on {self.date}"

    @classmethod
    def create_by_tag(cls, prospect_name, urls, tag):
        """Create 3 reports entries main, competitor one and competitor two all linked one prospect"""
        prospect = Prospect.objects.get(name=prospect_name)
        for url in urls:
            cls.objects.create(prospect=prospect, url=url, tag=tag)
