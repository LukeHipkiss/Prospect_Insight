from uuid import uuid4

from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from prospect.models import Prospect, Report
from prospect.queue import schedule_report


def index(request):
    context = {"prospects": Prospect.objects.all()}
    return render(request, "prospect/index.html", context)


def report(request):
    context = {"test": "This is a test context"}
    return render(request, "prospect/report.html", context)


def add_prospect(request):

    name = request.POST.get("name", "")

    if name:
        try:
            Prospect.objects.create(name=name)
        except IntegrityError:
            raise Http404(f"A prospect already exist called {name}")

    return HttpResponseRedirect(reverse("prospect:index"))


def generate_report(request):

    # Get the parameters of the form
    prospect = request.POST.get("prospect", "")
    prospect_url = request.POST.get("prospecturl", "")
    comp_one_url = request.POST.get("comp1url", "")
    comp_two_url = request.POST.get("comp2url", "")

    # Quick sanity check, so we don't mess the database
    if not all([prospect, prospect_url, comp_one_url, comp_two_url]):
        raise Http404(
            "Missing one of the parameters, ensure valid parameters have been passed."
        )

    # Setup things to store
    prospect_obj = Prospect.objects.get(name=prospect)
    uid = uuid4()

    schedule_report([prospect_url, comp_one_url, comp_two_url], uid, prospect_obj.name)

    # Create the 3 report entries to be compared. (I purposefully don't loop here)
    Report.objects.create(
        prospect=prospect_obj,
        url=prospect_url,
        tag=uid,
    )

    Report.objects.create(
        prospect=prospect_obj,
        url=comp_one_url,
        tag=uid,
    )

    Report.objects.create(
        prospect=prospect_obj,
        url=comp_two_url,
        tag=uid,
    )

    # Update the equivalent prospect row's number of reports and last time generated
    # The timestamp is updated every time the row is touched
    prospect_obj.reports += 1
    prospect_obj.last_tag = uid
    prospect_obj.save()

    return HttpResponseRedirect(reverse("prospect:index"))
