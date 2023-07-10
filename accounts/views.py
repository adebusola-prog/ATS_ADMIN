from django.shortcuts import render
from .serializers import LoginSerializer, ResetPasswordSerializer, SetNewPasswordSerializer
from .models import CustomUser
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.utils.encoding import force_bytes
from .utils import Utils
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend,\
      FilteringFilterBackend, SuggesterFilterBackend
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from .documents import CustomUserDocument
from .serializers import CustomUserDocumentSerializer

class CustomUserDocumentView(DocumentViewSet):
    document = CustomUserDocument
    serializer_class = CustomUserDocumentSerializer

    filter_backends = [
        # FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend
    ]

    search_fields = ('first_name', "last_name")
    
    suggester_fields = {
        'first_name': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
    }},

class LoginView(generics.GenericAPIView):
    authentication_classes = ()
    serializer_class =  LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(
            token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'refresh_token not provided.'}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful.'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class ForgotPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        lower_email = serializer.validated_data.get("email").lower()
        if CustomUser.objects.filter(email__iexact=lower_email).exists():
            account = CustomUser.objects.get(email=lower_email)
            uuidb64 = urlsafe_base64_encode(force_bytes(account.id))
            token = PasswordResetTokenGenerator().make_token(account)
            current_site = get_current_site(request).domain
            relative_path = reverse("authe:reset_password", kwargs={"uuidb64": uuidb64, "token": token})
            abs_url = "https://" + current_site + relative_path

            mail_subject = "Please Reset your Password"
            message = f"Hi {account.username}, please use the link below to reset your account password:\n{abs_url}"
            Utils.send_email(mail_subject, message, account.email)

            return Response({
                "status": "success",
                "message": "We have sent a password-reset link to the email you provided. Please check and reset."
            }, status=status.HTTP_200_OK)
        else:
            return Response({"email": ["User with this email does not exist."]}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
  
    def get(self, request, uuidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uuidb64))
            account = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(account, token):
                return Response({"status": "fail", "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "success", "message": "Your credentials valid", "uuidb64": uuidb64, "token": token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as e:
            return Response({"status": "fail", "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success", "message": "Password was successfully reset"}, status=status.HTTP_200_OK)

   