from django.db import models


class Prospect(models.Model):
    name = models.CharField(max_length=200, unique=True)
    reports = models.IntegerField(default=0)
    last = models.DateTimeField(auto_now=True)
    last_tag = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Report(models.Model):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=200)
    ref = models.URLField(max_length=200)

    def __str__(self):
        return f"Report for {self.prospect}, using url: {self.url} generated on {self.date}"
