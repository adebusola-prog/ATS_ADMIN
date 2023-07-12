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
    

class IsShortlistedOnlyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_shortlisted=True).\
            filter(is_invited_for_interview=False).filter(is_hired=False).\
            filter(is_rejected=False)
    
    
class InterviewInviteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_shortlisted=True).\
            filter(is_invited_for_interview=True)
    

class InterviewInviteOnlyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_shortlisted=True).\
            filter(is_invited_for_interview=True).filter(is_hired=False).\
            filter(is_rejected=False)
    

class HiredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_shortlisted=True).\
            filter(is_invited_for_interview=True).filter(is_hired=True).\
                filter(is_rejected=False)
    

class RejectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_shortlisted=True).\
            filter(is_invited_for_interview=True).filter(is_rejected=True).\
            filter(is_hired=False)