from django.test import TestCase
from django.urls import reverse
from .models import Reports
from users.models import Profile, User


class ReportListViewTests(TestCase):
    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user)

        # Create sample reports
        self.report1 = Reports.objects.create(
            owner=self.profile,
            title="Report 1",
            description="Description for report 1",
            status="Open",
        )
        self.report2 = Reports.objects.create(
            owner=self.profile,
            title="Report 2",
            description="Description for report 2",
            status="Closed",
        )

    def test_report_list_view_status_code(self):
        """Test if the report list view returns a 200 status code."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_report_list_view_template_used(self):
        """Test if the correct template is used for the report list view."""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "zvity/home.html")

    def test_report_list_view_context_data(self):
        """Test if all reports are included in the context."""
        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["reports"]), 2)
        self.assertIn(self.report1, response.context["reports"])
        self.assertIn(self.report2, response.context["reports"])

    def test_report_list_view_empty(self):
        """Test if the report list view handles no reports gracefully."""
        Reports.objects.all().delete()  # Clear all reports
        response = self.client.get(reverse("home"))
        self.assertContains(response, "No reports available.")
