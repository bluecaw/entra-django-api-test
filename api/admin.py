from django.contrib import admin

from api.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "address",
        "title",
        "status",
    )