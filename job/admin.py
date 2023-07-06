from django.contrib import admin
from .models import Job, JobApplication, Location
admin.site.register(Job)
admin.site.register(Location)
admin.site.register(JobApplication)
# Register your models here.
