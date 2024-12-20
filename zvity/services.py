from django.db import transaction
from .models import Reports


class ReportsUnitOfWork:
    def __init__(self, profile, data, files=None):
        self.profile = profile
        self.data = data
        self.files = files
        self.report = None

    def execute(self):
        with transaction.atomic():  # Ensures all operations are atomic
            self.report = self._create_report()
            return self.report

    def _create_report(self):
        report = Reports(
            owner=self.profile,
            title=self.data.get("title"),
            description=self.data.get("description"),
            status=self.data.get("status"),
        )
        if self.files and self.files.get("file_field_name"):
            report.some_file_field = self.files.get("file_field_name")
        report.save()
        return report
