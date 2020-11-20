from django.db import models


class Prospect(models.Model):
    name = models.CharField(max_length=200, unique=True)
    reports = models.IntegerField(default=0)
    last = models.DateTimeField(auto_now=True)
    last_tag = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @classmethod
    def update_last_report(cls, tag):
        """Update the prospect row's number of reports and last time generated
        The timestamp is updated every time the row is touched
        """
        report = Report.objects.get(tag=tag)
        prospect = report.prospect
        prospect.reports += 1
        prospect.last_tag = tag
        prospect.save()


class Report(models.Model):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    main_url = models.URLField(max_length=200)
    comp1_name = models.CharField(max_length=200, default="Competitor")
    comp1_url = models.URLField(max_length=200)
    comp2_name = models.CharField(max_length=200, default="Competitor")
    comp2_url = models.URLField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"Report for {self.prospect} generated on {self.date}"

    @classmethod
    def create_by_tag(cls, prospect_name, comp1_name, comp2_name, urls, tag):
        """Creates a report """
        prospect = Prospect.objects.get(name=prospect_name)
        main_url, comp1_url, comp2_url = urls
        cls.objects.create(
            prospect=prospect,
            main_url=main_url,
            comp1_name=comp1_name,
            comp1_url=comp1_url,
            comp2_name=comp2_name,
            comp2_url=comp2_url,
            tag=tag
        )
