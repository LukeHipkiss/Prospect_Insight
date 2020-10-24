from django.contrib import admin  # noqa: F401

from .models import Report, Prospect
# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    pass


class ProspectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Report, ReportAdmin)
admin.site.register(Prospect, ProspectAdmin)
