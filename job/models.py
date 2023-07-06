import os
from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.timesince import timesince
from base.managers import ActiveManager, InActiveManager
# from cities_light.models import City


def validate_pdf_file(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    if ext.lower() != '.pdf':
        raise ValidationError("Only PDF files are allowed.")


class Location(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

SKILL_LEVEL_CHOICES = (
    ('Junior', 'Junior'),
    ('Senior', 'Senior'),
    ('Mid-level', 'Mid-level'),
)

JOB_TYPE_CHOICES = (
    ('On-site', 'On-site'),
    ('Remote', 'Remote'),
    ('Hybrid', 'Hybrid'),
)

JOB_SCHEDULE_CHOICES = (
    ('Full-time', 'Full-time'),
    ('Project-based', 'Project-based'),
)
    
class Job(models.Model):
    role = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    job_schedule = models.CharField(max_length=20, choices=JOB_SCHEDULE_CHOICES)
    job_requirements = models.TextField()
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.ManyToManyField(Location, related_name='job_locations')
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()
    
    def __str__(self):
        return self.role

    def time_since_creation(self):
        time_difference = timezone.now() - self.created_at
        if time_difference.total_seconds() < 60:
            return "uploaded now"
        return f"Uploaded {timesince(self.created_at, timezone.now())} ago"


class JobApplication(models.Model):
    job = models.ManyToManyField(Job, related_name='applications')
    applicant = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/', validators=[validate_pdf_file], null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    is_shortlisted = models.BooleanField(default=False)
    is_invited_for_assessment = models.BooleanField(default=False)
    is_invited_for_interview = models.BooleanField(default=False)
    is_hired = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

