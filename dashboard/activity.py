import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import ActivityLog, READ, CREATE, UPDATE, DELETE, SUCCESS, FAILED


class ActivityLogJobMixin:
    """Retrieve the user from the request."""
    def _get_user(self, request):
        user = request.user if request.user.is_authenticated else None
        return user

    def _create_activity_log(self, instance, request):
        actor = self._get_user(request)
        message = f"New job created "
        ActivityLog.objects.create(actor=actor, action_type=CREATE, content_object=instance, data=message)

    def _update_activity_log(self, instance, request, old_role):
        actor = self._get_user(request)
        message = f"{old_role} was updated "
        ActivityLog.objects.create(actor=actor, action_type=UPDATE, content_object=instance, 
                        data=message)

    def _delete_activity_log(self, instance, old_role, request):
        actor = self._get_user(request)
        message = f"{old_role} deleted "
        ActivityLog.objects.create(actor=actor, action_type=DELETE, content_object=instance, data=message)

    def _create_application_activity_log(self, instance, request):
        actor = self._get_user(request)
        message = f"New job Application "
        ActivityLog.objects.create(actor=actor, action_type=CREATE, content_object=instance, data=message)
