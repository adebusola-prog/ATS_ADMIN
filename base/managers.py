from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)
    

class IsShortlistedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_shortlisted=True)
    
class IsShortlistedInterviewInviteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_shortlisted=True).filter(is_invited_for_interview=True)