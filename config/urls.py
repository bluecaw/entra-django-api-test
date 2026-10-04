from django.contrib import admin
from django.urls import path

from api.views import HealthView, AuthTestView, ReportListView, CreateReportView, DeleteReportView, UpdateReportView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", HealthView.as_view()),
    path("api/test/auth/", AuthTestView.as_view()),
    path("api/reports/", ReportListView.as_view()),
    path("api/reports/create/", CreateReportView.as_view()),
    path("api/reports/<int:pk>/",DeleteReportView.as_view()),
    path("api/reports/<int:pk>/",UpdateReportView.as_view()
),
]