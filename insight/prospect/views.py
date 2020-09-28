from django.shortcuts import render


def index(request):
    context = {"test": "This is a test context"}
    return render(request, 'prospect/index.html', context)


def report(request):
    context = {"test": "This is a test context"}
    return render(request, 'prospect/report.html', context)
