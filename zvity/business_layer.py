# zvity/business_logic.py
from django.core.exceptions import PermissionDenied
from .models import Reports


def can_delete_report(user, report: Reports) -> bool:
    """
    Business logic to check if a user can delete a report.
    Returns True if the user is allowed to delete the report,
    otherwise raises PermissionDenied exception.
    """
    if user.is_staff:  # Staff can delete any report
        return True
    if report.owner == user.profile:  # Owner can delete their own report
        return True
    raise PermissionDenied("You do not have permission to delete this report.")


def can_change_status(user, report):
    """Check if a user can change the status of a report."""
    if not user.is_staff:
        raise PermissionDenied(
            "You do not have permission to change the report status."
        )
    return True
