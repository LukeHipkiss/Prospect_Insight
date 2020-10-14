from uuid import uuid4

from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from prospect.models import Prospect, Report
from prospect.queue import schedule_report, q as queue


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
            messages.error(request, f"A prospect already exist called {name}")

    return HttpResponseRedirect(reverse("prospect:index"))


def generate_report(request):

    if request.session.get("ongoing_report"):
        messages.info(request, "You already have a running report, wait for it to finish before starting a new one.")
        return HttpResponseRedirect(reverse("prospect:index"))

    # Get the parameters of the form
    prospect = request.POST.get("prospect", "")
    prospect_url = request.POST.get("prospecturl", "")
    comp_one_url = request.POST.get("comp1url", "")
    comp_two_url = request.POST.get("comp2url", "")

    # Setup identifiers
    prospect_obj = Prospect.objects.get(name=prospect)
    uid = uuid4()

    # Run background work and store job ids in current session
    main, comp1, comp2 = schedule_report([prospect_url, comp_one_url, comp_two_url], uid, prospect_obj.name)
    request.session["ongoing_report"] = True
    request.session["main_id"] = main
    request.session["comp1_id"] = comp1
    request.session["comp2_id"] = comp2

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

    # Update the prospect row's number of reports and last time generated
    # The timestamp is updated every time the row is touched
    prospect_obj.reports += 1
    prospect_obj.last_tag = uid
    prospect_obj.save()

    messages.info(request, "Your report is being prepared!")
    return HttpResponseRedirect(reverse("prospect:index"))


def check_report_status(request):
    main = request.session.get("main_id")
    comp1 = request.session.get("comp1_id")
    comp2 = request.session.get("comp2_id")
    jobs = [main, comp1, comp2]

    if {main, comp1, comp2}.issubset(queue.finished_job_registry.get_job_ids()):
        clear = True
        messages.info(request, "Your report is ready!")

    elif {main, comp1, comp2}.issubset(queue.failed_job_registry.get_job_ids()):
        clear = True
        messages.info(request, "Unfortunately there has been a problem generating your report, tell Luke!")
    elif any(job in jobs for job in queue.scheduled_job_registry.get_job_ids()):
        return JsonResponse({"response": "Your report is waiting to be processed", "status": "Busy"})
    elif any(job in jobs for job in queue.started_job_registry.get_job_ids()):
        return JsonResponse({"response": "Your report is being processed", "status": "Busy"})
    elif any(job in jobs for job in queue.deferred_job_registry.get_job_ids()):
        return JsonResponse({"response": "Your report has been deferred", "status": "Busy"})
    else:
        clear = True
        messages.info(request, "We were unable to find your report request")

    if clear:
        request.session["ongoing_report"] = False
        request.session["main_id"] = ""
        request.session["comp1_id"] = ""
        request.session["comp2_id"] = ""
        return JsonResponse({"response": "Free to go!", "status": "Available"})
