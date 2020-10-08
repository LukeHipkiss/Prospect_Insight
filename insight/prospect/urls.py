from django.urls import path

from . import views

app_name = "prospect"
urlpatterns = [
    path("", views.index, name="index"),
    path("report", views.report, name="report"),
    path("add", views.add_prospect, name="add"),
    path("analyse", views.generate_report, name="analyse"),
]
