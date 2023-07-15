from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser
from . import config
from datetime import date

class AdminAccountTests(TestCase):
    """Test the accounts in the Django admin interface"""

    def setUp(self):
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create_user(
            username=config.ADMIN_USERNAME,
            email=config.ADMIN_EMAIL,
            password=config.ADMIN_PASSWORD,
            first_name = "Tella",
            last_name = "Oke",
            date_of_birth=date(1990, 5, 15) 

        )

    def test_create_user(self):
        """Test creating a user from Django admin"""
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse("authe:log_in"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "email": config.ADMIN_EMAIL,
            "password": config.ADMIN_PASSWORD,
        }
        response = self.client.post(reverse("authe:log_in"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_password_too_short(self):
        """Test that password is too short"""
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse("authe:log_in"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "email": config.ADMIN_EMAIL,
            "password": "pw", 
        }
        response = self.client.post(reverse("authe:log_in"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
