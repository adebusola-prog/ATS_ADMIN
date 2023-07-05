from rest_framework import serializers
from cities_light.models import City
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    STATE_CHOICES = [
        (city.id, city.name) for city in City.objects.filter(country__name='Nigeria')
    ]
    
    states = serializers.MultipleChoiceField(choices=STATE_CHOICES)

    class Meta:
        model = Job
        fields = '__all__'