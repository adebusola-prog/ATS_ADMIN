from django.db import models
from accounts.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.timesince import timesince
from django.utils import timezone


CREATE, READ, UPDATE, DELETE = "Create", "Read", "Update", "Delete"
LOGIN, LOGOUT, LOGIN_FAILED = "Login", "Logout", "Login Failed"
ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]

SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]


class ActivityLog(models.Model):
    """
    Model representing an activity log.
    """
    actor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=15)
    action_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(choices=ACTION_STATUS, max_length=7, default=SUCCESS)
    data = models.JSONField(default=dict)
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    def __str__(self):
        return f"{self.action_type} by {self.actor} on {self.action_time}"

    def get_timesince(self):
        time_difference = timezone.now() - self.action_time
        if time_difference.total_seconds() < 60:
            return "now"
        elif time_difference.total_seconds() < 86400:
            timesince_str = timesince(self.action_time, timezone.now())
            timesince_str = timesince_str.replace('minutes', 'min').replace('hours', 'hr')
            hours_str = timesince_str.split(",")[0].strip()
            return f"{hours_str} ago"
        
        days = time_difference.days
        if days == 1:
            return "1 day ago"
        else:
            return f"{days} days ago"
        
