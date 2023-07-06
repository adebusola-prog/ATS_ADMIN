from rest_framework import serializers
from .models import Job, Location, JobApplication
from rest_framework.reverse import reverse

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name',)


class JobSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    update_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()
    uploaded_time = serializers.CharField(source='time_since_creation', read_only=True)
    posted_by = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ('detail_url', 'update_url', 'delete_url', 'role', 'skill_level', 
                'job_type', 'job_schedule', 'job_requirements', 'posted_by', 'uploaded_time', 'location')
        
        extra_kwargs = {
            'skill_level': {"write_only": True},
            'posted_by': {"read_only": True},
        }
    
    def get_detail_url(self, obj):
        request = self.context.get('request')
        absolute_url = reverse('job_detail_update', args=[str(obj.id)], request=request)
        return absolute_url
        
    def get_update_url(self, obj):
        request = self.context.get('request')
        update_url = reverse('job_detail_update', args=[str(obj.id)], request=request)
        return update_url
    
    def get_delete_url(self, obj):
        request = self.context.get('request')
        delete_url =  reverse('job_delete', args=[str(obj.id)], request=request)
        return delete_url

class JobApplicationListCreateSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    applicant = serializers.CharField(source='applicant.get_full_name', read_only=True)
    short_name = serializers.CharField(source='applicant.get_short_name', read_only=True)

    class Meta:
        model = JobApplication
        fields = ('detail_url', 'job', 'applicant', 'cover_letter', 'resume', 'short_name')

    def get_detail_url(self, obj):
        request = self.context.get('request')
        absolute_url = reverse('job_application_detail', args=[str(obj.id)], request=request)
        return absolute_url