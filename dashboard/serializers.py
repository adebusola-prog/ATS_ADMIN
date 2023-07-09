from rest_framework import serializers
from .models import ActivityLog
from accounts.models import CustomUser
from ats_admin.serializers import CustomUserSubAdminSerializer

class ActivityLogSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    
    class Meta:
        model = ActivityLog
        fields = ('action_type','get_timesince', 'status', 'content_type','data')

    # def get_actor(self, obj):
    #     actor = obj.posted_by.actor
    #     if actor is not None:
    #         user_id = actor.id
    #         user = CustomUser.objects.get(id=user_id)
    #         serializer = CustomUserSubAdminSerializer(user, context=self.context)
    #         first_name = serializer.data['first_name']
    #         last_name = serializer.data['last_name']
    #         return first_name + ' ' + last_name
    #     return None

    def get_content_type(self, obj):
        content_type = obj.content_type
        if content_type is not None:
            return content_type.model
        return None