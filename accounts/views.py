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
from .utils import Utils
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


# class LogoutView(APIView):
#     def post(self, request, *args, **kwargs):
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('access_token')
        if not refresh_token:
            return Response({'error': 'refresh_token not provided.'}, status=400)

        try:
            token = AccessToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful.'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class ForgotPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            lower_email = serializer.validated_data.get("email").lower()
            # if CustomUser.objects.filter(email__iexact=lower_email).exists():
            account = CustomUser.objects.get(email=lower_email)
            uuidb64 = urlsafe_base64_encode(account.id)
            token = PasswordResetTokenGenerator().make_token(account)
            current_site = get_current_site(
                request).domain
            relative_path = reverse(
                "reset-password", kwargs={"uuidb64": uuidb64, "token": token})
            abs_url = "http://" + current_site + relative_path

            mail_subject = "Please Reset your CustomUser Password"
            message = "Hi" + account.username + "," + \
                " Please Use the Link below to reset your account passwors:" + "" + abs_url
            Utils.send_email(mail_subject, message, account.email)
            return Response({"status": "success", "message": "We have sent a password-reset link to the email you provided.Please check and reset  "}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
  
    def get(self, request, uuidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uuidb64))
            account = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(account, token):
                return Response({"status": "fail", "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "success", "message": "Your credentials valid", "uuidb64": uuidb64, "token": token}, status=status.HTTP_400_BAD_REQUEST)
        except DjangoUnicodeDecodeError as e:
            return Response({"status": "fail", "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer