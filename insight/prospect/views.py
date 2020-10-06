from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from prospect.models import Prospect


def index(request):
    context = {"prospects": Prospect.objects.all()}
    return render(request, 'prospect/index.html', context)


def report(request):
    context = {"test": "This is a test context"}
    return render(request, 'prospect/report.html', context)


def add_prospect(request):

    name = request.POST.get("name", "")

    if name:
        try:
            Prospect.objects.create(name=name)
        except IntegrityError:
            raise Http404(f"A prospect already exist called {name}")

    return HttpResponseRedirect(reverse("prospect:index"))
