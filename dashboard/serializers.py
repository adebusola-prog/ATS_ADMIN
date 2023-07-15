from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    """
    Serializer for the ActivityLog model.
    """
    actor = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    
    class Meta:
        model = ActivityLog
        fields = ("actor", 'action_type','get_timesince', 'status', 'content_type','data')

    def get_actor(self, obj):
        actor = obj.actor
        if actor:
            return f"{actor.first_name} {actor.last_name}"
        return None

    def get_content_type(self, obj):
        content_type = obj.content_type
        if content_type is not None:
            return content_type.model
        return None