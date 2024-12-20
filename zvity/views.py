from django.shortcuts import render, redirect
from .forms import ReportsForm
from .services import ReportsUnitOfWork
from .models import Reports


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


def report_list(request):
    reports = Reports.objects.all()
    return render(request, "zvity/home.html", {"reports": reports})
