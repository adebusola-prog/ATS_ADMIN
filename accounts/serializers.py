from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
# from .documents import CustomUserDocument

from .models import CustomUser, PermissionLevel


# class CustomUserDocumentSerializer(DocumentSerializer):
#     class Meta:
#         document = CustomUserDocument

#         fields = (
#             'first_name',
#             'last_name'
#             'get_full_name'
#         )

class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for user login.
    """
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    is_admin = serializers.BooleanField(read_only=True)
    is_superadmin = serializers.BooleanField(read_only=True)
    # profile_picture = serializers.FileField(read_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ("email", "password", "first_name", "last_name", "is_admin", "is_superadmin", "role")
                #  "profile_picture"


    def validate(self, validated_data):
        user = authenticate(**validated_data)
        if not user.is_active:
            raise serializers.ValidationError("You have been suspended")
        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_admin'] = instance.is_admin
        representation['is_superadmin'] = instance.is_superadmin
        return representation
    
    def get_role(self, user):
        if user.is_admin:
            return 'is_admin'
        elif user.is_superadmin:
            return 'is_superadmin'
        else:
            return None
     

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()

    class Meta:
        fields = ('email',)

   
    # def validate_email(self, value):
    #     lower_email = value.lower()

        # return lower_email


class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=1, write_only=True)
    uuidb64 = serializers.CharField(min_length=1, write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    # class Meta:
    #     fields = ("password", "confirm_password", "token", "uuidb64")

    def validate(self, attrs):
        try:
            if attrs.get('password') != attrs.get('confirm_password'):
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."})
            token = attrs.get('token')
            uuidb64 = attrs.get('uuidb64')

            id = force_str(urlsafe_base64_decode(uuidb64))
            account = CustomUser.active_objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(account, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            account.set_password(attrs.get('password'))
            account.save()
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


class PermissionLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionLevel
        fields = ('id', 'name')
