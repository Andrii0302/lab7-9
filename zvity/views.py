from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReportsForm
from .services import ReportsUnitOfWork
from .models import Reports
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .business_layer import can_delete_report


@login_required
def create_report(request):
    profile = request.user.profile
    form = ReportsForm()

    if request.method == "POST":
        form = ReportsForm(request.POST, request.FILES)
        if form.is_valid():
            uow = ReportsUnitOfWork(profile, request.POST, request.FILES)
            uow.execute()
            return redirect("home")

    context = {"form": form}
    return render(request, "zvity/create_report.html", context)


@login_required
def report_list(request):
    if request.user.is_staff:
        reports = Reports.objects.all()
    else:
        reports = Reports.objects.filter(owner=request.user.profile)

    return render(request, "zvity/home.html", {"reports": reports})


@login_required
def delete_report(request, report_id):
    report = get_object_or_404(Reports, id=report_id)

    try:
        # Check if the user can delete the report using the business layer function
        can_delete_report(request.user, report)

        if request.method == "POST":
            report.delete()
            return redirect("home")
        return render(request, "zvity/delete_report.html", {"report": report})

    except PermissionDenied as e:
        # Handle the case where the user is not authorized to delete the report
        return render(request, "zvity/permission_denied.html", {"error": str(e)})
