from rest_framework import serializers
from accounts.models import CustomUser
from rest_framework.reverse import reverse
from django.contrib.auth.password_validation import validate_password


class CustomUserSuperAdminSerializer(serializers.ModelSerializer):
    admin = serializers.CharField(source='admin_status', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'first_name', 'last_name', 'email', 'position', 'admin', 'profile_picture')

        extra_kwargs = {
            'position': {'write_only': True},
            'email': {'write_only': True}
        }


class CustomUserPictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('profile_picture',)


class CustomUserSubAdminSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('detail_url','full_name', 'first_name', 'last_name', 'username', 'email',  'profile_picture', 'position',
                  'permission_level', 'password', 'confirm_password')
        extra_kwargs = {
            'position': {'required': True},
            'permission_level': {'required': True},
        }

    def get_detail_url(self, obj):
        request = self.context.get('request')
        absolute_url = reverse('ats:sub_admin_detail', args=[str(obj.id)], request=request)
        return absolute_url
        
    
    def validate(self, attrs):
        if not attrs['position']:
            raise serializers.ValidationError({"position": "Sub Admin's position is required."})
        if not attrs['permission_level']:
            raise serializers.ValidationError({"permission_level": "Sub Admin's permission level is required."})
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        permission_level_data = validated_data.pop('permission_level')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.is_admin = True
        instance.save()
        instance.permission_level.set(permission_level_data)
        return instance

    def perform_create(self, validated_data):
        validated_data['is_admin'] = True 
        return super().perform_create(validated_data)
    
