from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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