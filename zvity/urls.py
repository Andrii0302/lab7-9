from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.report_list, name="home"),
    path("create-report/", views.create_report, name="create_report"),
    path("report/<uuid:report_id>/delete/", views.delete_report, name="delete-report"),
]
