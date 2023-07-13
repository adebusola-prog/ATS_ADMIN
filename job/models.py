import os
from django.db import models
from django.db.models import Sum
from accounts.models import CustomUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.timesince import timesince
from base.managers import ActiveManager, InActiveManager, IsShortlistedManager, \
    InterviewInviteManager, HiredManager, RejectedManager, IsShortlistedOnlyManager,\
    InterviewInviteOnlyManager

# from cities_light.models import City


def _json_list():
    return list

def validate_pdf_file(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.pdf':
        raise ValidationError("Only PDF files are allowed.")


class Location(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}_{self.id}"

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
    no_of_views = models.IntegerField(default=0, blank=True)
    
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

    def views_count(self):
        total_views = Job.objects.aggregate(total_views=Sum('no_of_views'))['total_views']
        return total_views
    
    def get_total_applications(self):
        return self.applications.count()
    


class JobViews(models.Model):
    job = models.ForeignKey(Job, related_name="job_views", on_delete=models.SET_NULL, null=True)
    viewer_ip = models.JSONField(default=_json_list())
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
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
    shortlisted_objects = IsShortlistedManager()
    shortlisted_only_objects = IsShortlistedOnlyManager()
    interview_objects = InterviewInviteManager()
    interview_only_objects = InterviewInviteOnlyManager()
    hired_objects = HiredManager()
    rejected_objects = RejectedManager()

    def __str__(self):
        return f"{self.id}/{self.applicant.email}'s applicantion for {self.job}"
    
    @classmethod
    def get_total_applicants(cls):
        return JobApplication.active_objects.count()

class InterviewInvitation(models.Model):
    job_application = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()