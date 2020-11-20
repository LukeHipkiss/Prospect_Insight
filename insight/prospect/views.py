from uuid import uuid4

from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from prospect.models import Prospect, Report
from prospect.queue import schedule_report, q as queue
from prospect.s3 import get_json_reports


def index(request):
    context = {"prospects": Prospect.objects.all()}
    return render(request, "prospect/index.html", context)


def report(request, report_tag):

    rep = Report.objects.get(tag=report_tag)

    reports_data = get_json_reports(rep)

    context = {
        "prospect": rep.prospect.name,
        "comp1": rep.comp1_name,
        "comp2": rep.comp2_name,
        "reports": reports_data,
        "tag": report_tag
    }
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

    # Get parameters from the form
    prospect = request.POST.get("prospect", "")
    prospect_url = request.POST.get("prospecturl", "")
    comp_one_name = request.POST.get("comp1name", "")
    comp_one_url = request.POST.get("comp1url", "")
    comp_two_name = request.POST.get("comp2name", "")
    comp_two_url = request.POST.get("comp2url", "")

    # Create a unique tag
    tag = uuid4()

    # Add reports to the queue to be picked up by workers
    main, comp1, comp2 = schedule_report([prospect_url, comp_one_url, comp_two_url], tag, prospect)

    # Store session information
    request.session["ongoing_report"] = True
    request.session["main_id"] = main
    request.session["comp1_id"] = comp1
    request.session["comp2_id"] = comp2
    request.session["tag"] = str(tag)

    # Update db
    Report.create_by_tag(prospect, comp_one_name, comp_two_name, [prospect_url, comp_one_url, comp_two_url], tag)

    messages.info(request, "Your report is being prepared!")
    return HttpResponseRedirect(reverse("prospect:index"))


def check_report_status(request):

    #  Retrieve session info
    main = request.session.get("main_id")
    comp1 = request.session.get("comp1_id")
    comp2 = request.session.get("comp2_id")
    tag = request.session.get("tag")
    jobs = [main, comp1, comp2]

    if {main, comp1, comp2}.issubset(queue.finished_job_registry.get_job_ids()):
        messages.info(request, "Your report is ready!")
        Prospect.update_last_report(tag)

    elif {main, comp1, comp2}.issubset(queue.failed_job_registry.get_job_ids()):
        messages.info(request, "There has been a problem creating your report.")

    elif any(job in jobs for job in queue.scheduled_job_registry.get_job_ids()):
        return JsonResponse({"response": "Your report is waiting to be processed", "status": "Busy"})
    elif any(job in jobs for job in queue.started_job_registry.get_job_ids()):
        return JsonResponse({"response": "Your report is being processed", "status": "Busy"})
    elif any(job in jobs for job in queue.deferred_job_registry.get_job_ids()):
        return JsonResponse({"response": "Your report has been deferred", "status": "Busy"})
    else:
        messages.info(request, "We were unable to find your report request")

    # If the job is finished or failed or we can't find it, flush the session and free the user.
    request.session.flush()
    return JsonResponse({"response": "Free to go!", "status": "Available"})
