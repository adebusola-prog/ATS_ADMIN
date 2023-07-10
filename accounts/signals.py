from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry
from .documents import CustomUserDocument
from .models import CustomUser



@receiver(post_save, sender=CustomUser)
def update_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']
    
    if app_label == 'accounts':
        if model_name == 'customuser':
            instances = instance.customuser.all()
            for _instance in instances:
                registry.update(_instance)
    
@receiver(post_delete, sender=CustomUser)
def delete_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']
    
    if app_label == 'accounts':
        if model_name == 'customuser':
            instances = instance.customuser.all()
            for _instance in instances:
                registry.update(_instance)