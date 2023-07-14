import logging
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError
from .models import ActivityLog, READ, CREATE, UPDATE, DELETE, SUCCESS, FAILED
from django.utils import timezone



class ActivityLogJobMixin:
    def _get_user(self, request):
        user = request.user if request.user.is_authenticated else None
        return user


    def _create_activity_log(self, instance, request):
        actor = self._get_user(request)
        message = f"New job created by {instance.posted_by.first_name} {instance.posted_by.last_name}"
        ActivityLog.objects.create(actor=actor, action_type=CREATE, content_object=instance, data=message)


    def _update_activity_log(self, instance, request, old_role):
        actor = self._get_user(request)
        # current_time = timezone.now()
        message = f"{old_role} was updated by {instance.posted_by.first_name} {instance.posted_by.last_name}"
        ActivityLog.objects.create(actor=actor, action_type=UPDATE, content_object=instance, 
                        data=message)


    def _delete_activity_log(self, instance, request):
        actor = self._get_user(request)
        message = f"{instance.role} deleted by {instance.posted_by.first_name} {instance.posted_by.last_name}"
        ActivityLog.objects.create(actor=actor, action_type=DELETE, content_object=instance, data=message)


    def _create_application_activity_log(self, instance, request):
        actor = self._get_user(request)
        message = f"New job Application by {request.user.first_name}{request.user.first_name}"
        ActivityLog.objects.create(actor=actor, action_type=CREATE, content_object=instance, data=message)
