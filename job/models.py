from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from django.utils.timesince import timesince
from cities_light.models import City
# Create your models here.


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

STATE_CHOICES = [
        (city.id, city.name) for city in City.objects.filter(country__name='Nigeria')
    ]
    
class Job(models.Model):
    title = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    job_schedule = models.CharField(max_length=20, choices=JOB_SCHEDULE_CHOICES)
    job_requirements = models.TextField()
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, choices=STATE_CHOICES)

    def __str__(self):
        return self.title

    def time_since_creation(self):
        return f"{timesince(self.created_at, timezone.now())} ago"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)


