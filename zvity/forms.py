from django import forms
from .models import Reports
from django.forms import ModelForm


class ReportsForm(ModelForm):
    class Meta:
        model = Reports
        fields = "__all__"
        exclude = ["owner", "status"]
