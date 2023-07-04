from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth.password_validation import validate_password


class CustomUserSuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'position', "is_superadmin")


class CustomUserUserPictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('profile_picture',)


class CustomUserSubAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'position', 'permission_level', 'password', 'confirm_password']
        extra_kwargs = {
            'position': {'required': True},
            'permission_level': {'required': True}
        }
    
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

        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.is_admin = True
        instance.save()
        return instance
    
    def perform_create(self, validated_data):
        validated_data['is_admin'] = True 
        return super().perform_create(validated_data)