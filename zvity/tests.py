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
        self.client.login(username="testuser", password="password")  # Login the user
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_report_list_view_template_used(self):
        """Test if the correct template is used for the report list view."""
        self.client.login(username="testuser", password="password")  # Login the user
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "zvity/home.html")

    def test_report_list_view_context_data(self):
        """Test if all reports are included in the context."""
        self.client.login(username="testuser", password="password")  # Login the user
        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["reports"]), 2)
        self.assertIn(self.report1, response.context["reports"])
        self.assertIn(self.report2, response.context["reports"])

    def test_report_list_view_empty(self):
        """Test if the report list view handles no reports gracefully."""
        Reports.objects.all().delete()  # Clear all reports
        self.client.login(username="testuser", password="password")  # Login the user
        response = self.client.get(reverse("home"))
        self.assertContains(response, "No reports available.")


from django.core.exceptions import PermissionDenied
from .business_layer import can_delete_report


class ReportBusinessLogicTests(TestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username="user", password="password")
        self.user.profile = Profile.objects.create(user=self.user)
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.staff_user.profile = Profile.objects.create(user=self.staff_user)

        # Create a report owned by the regular user
        self.report = Reports.objects.create(
            owner=self.user.profile,
            title="User's Report",
            description="User's report description",
            status="Open",
        )

    def test_can_delete_report_owner(self):
        """Test that the owner can delete their own report."""
        result = can_delete_report(self.user, self.report)
        self.assertTrue(result)

    def test_can_delete_report_staff(self):
        """Test that a staff member can delete any report."""
        result = can_delete_report(self.staff_user, self.report)
        self.assertTrue(result)

    def test_cannot_delete_report_forbidden(self):
        """Test that a non-owner and non-staff user cannot delete the report."""
        non_owner_user = User.objects.create_user(
            username="non_owner", password="password"
        )
        non_owner_user.profile = Profile.objects.create(user=non_owner_user)

        with self.assertRaises(PermissionDenied):
            can_delete_report(non_owner_user, self.report)

    def test_business_logic_permission_denied(self):
        """Test that PermissionDenied is raised when a non-authorized user tries to delete."""
        non_owner_user = User.objects.create_user(
            username="non_owner", password="password"
        )
        non_owner_user.profile = Profile.objects.create(user=non_owner_user)

        with self.assertRaises(PermissionDenied):
            can_delete_report(non_owner_user, self.report)


class ReportStatusChangeTestCase(TestCase):
    def setUp(self):
        """Set up users and a sample report."""
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username="regular", password="password"
        )

        # Create profiles manually for the users
        self.staff_user.profile = Profile.objects.create(user=self.staff_user)
        self.regular_user.profile = Profile.objects.create(user=self.regular_user)

        # Create a sample report
        self.report = Reports.objects.create(
            title="Test Report",
            description="This is a test report.",
            status="Open",
            owner=self.regular_user.profile,
        )

    def test_staff_can_change_status(self):
        """Test that a staff user can change the status of a report."""
        self.client.login(username="staff", password="password")
        response = self.client.post(
            reverse("change-report-status", args=[self.report.id]), {"status": "Closed"}
        )
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, "Closed")
        self.assertRedirects(response, reverse("home"))
