from django.shortcuts import render


def index(request):
    context = {"test": "This is a test context"}
    return render(request, 'prospect/index.html', context)
