from django.contrib import admin
from .models import Job, JobApplication, Location
admin.site.register(Location)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('role', 'posted_by', 'created_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('role', 'posted_by__username')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'applicant', 'applied_at', 'is_shortlisted', 'is_invited_for_interview', 'is_hired')
    list_filter = ('is_shortlisted', 'is_invited_for_interview', 'is_hired')
    search_fields = ('job__role', 'applicant__username')

