from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import gettext_lazy as _



class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for user login.
    """

    @classmethod
    def get_token(cls, user):
        """
        Retrieves the token for the authenticated user and adds custom claims.
        """
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

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

    class Meta:
        fields = ("password", "confirm_password", "token", "uuidb64")

    def validate(self, attrs):
        try:
            if attrs.get('password') != attrs.get('confirm_password'):
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."})
            token = attrs.get('token')
            uuidb64 = attrs.get('uuidb64')

            id = force_str(urlsafe_base64_decode(uuidb64))
            account = CustomUser.objects.get(id=id)

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