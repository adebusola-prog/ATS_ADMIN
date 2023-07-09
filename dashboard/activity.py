import logging
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError
from .models import ActivityLog, READ, CREATE, UPDATE, DELETE, SUCCESS, FAILED


# class ActivityLogMixin:
#     """Mixins to track activity"""

#     log_message = None

#     def _get_action_type(self, request):
#         return self.action_type_mapper().get(f"{request.method.upper()}")

#     def _build_log_message(self, request):
#         user=self._get_user(request)
#         first_name=user.first_name
#         last_name = user.last_name
#         return f" {first_name} {last_name}  {self._get_action_type(request)} {request.resolver_match.url_name}"

#     def get_log_message(self, request):
#         return self.log_message or self._build_log_message(request)

#     @staticmethod
#     def action_type_mapper():
#         return {
#             "GET": READ,
#             "POST": CREATE,
#             "PUT": UPDATE,
#             "PATCH": UPDATE,
#             "DELETE": DELETE,
#         }

#     @staticmethod
#     def _get_user(request):
#         return request.user if request.user.is_authenticated else None

#     def _write_log(self, request, response):
#         status = SUCCESS if response.status_code < 400 else FAILED
#         actor = self._get_user(request)

#         if actor and not getattr(settings, "TESTING", False):
#             logging.info("Started Log Entry")

#             data = {
#                 "actor": actor,
#                 "action_type": self._get_action_type(request),
#                 "status": status,
#                 # "remarks": self.get_log_message(request),
#             }
#             try:
#                 data["content_type"] = ContentType.objects.get_for_model(
#                     self.get_queryset().model
#                 )
#                 data["content_object"] = self.get_object()
#             except (AttributeError, ValidationError):
#                 data["content_type"] = None
#             except AssertionError:
#                 pass
#             object= self.get_object()
#             print('Object:', type(object))
#             message = f"{self._get_action_type(request)} {object.first_name} {object.last_name}"
#             print(message)
#             ActivityLog.objects.create(**data, data=message)

#     def finalize_response(self, request, *args, **kwargs):
#         response = super().finalize_response(request, *args, **kwargs)
#         self._write_log(request, response)
#         return response


class ActivityLogJobMixin:
    def _get_user(self, request):
        user = request.user if request.user.is_authenticated else None
        return user

    def _create_activity_log(self, instance, request):
        actor = self._get_user(request)
        message = f"New job created by {instance.posted_by.first_name} {instance.posted_by.last_name}"
        ActivityLog.objects.create(actor=actor, action_type=CREATE, content_object=instance, data=message)

    def _update_activity_log(self, instance, request):
        actor = self._get_user(request)
        old_instance = self.queryset.get(pk=instance.pk)
        old_role = old_instance.role 
        message = f"{old_role} updated by {instance.posted_by.first_name} {instance.posted_by.last_name}"
        ActivityLog.objects.create(actor=actor, action_type=UPDATE, content_object=instance, data=message)


    def _delete_activity_log(self, instance, request):
        actor = self._get_user(request)
        message = f"{instance.role} deleted by {instance.posted_by.first_name} {instance.posted_by.last_name}"
        ActivityLog.objects.create(actor=actor, action_type=DELETE, content_object=instance, data=message)