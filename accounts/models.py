from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from .validators import validate_image_size
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError
from datetime import date
from base.constants import BACKEND_DEVELOPER, PRODUCT_MANAGER, MOBILE_DEVELOPER, FRONTEND_DEVEOPER
from base.managers import ActiveManager, InActiveManager


def validate_date_of_birth(value):
    today = date.today()
    age_limit = today.replace(year=today.year - 18)
    
    if value >= age_limit:
        raise ValidationError("You must be at least 18 years old.")
    
# class MyAccountManager(BaseUserManager):
#     def create_user(self, first_name, last_name, username, email, password=None, is_superadmin=False):
#         if not username:
#             raise ValueError("User must have a username")
#         if not email:
#             raise ValueError("User must have an email address")
        
#         user = self.model(username=username, first_name=first_name, last_name=last_name, 
#                           email=self.normalize_email(email))
#         user.set_password(password)
#         user.is_superadmin = is_superadmin  # Set the is_superadmin status
#         user.save(using=self._db)
#         return user
       

#     def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
#         """ creates superuser"""
#         extra_fields.setdefault("is_superadmin", True)
        
#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
        
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")
        
#         return self.create_user(first_name, last_name, email=email, password=password, **extra_fields)

class PermissionLevel(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    """Custom User Model that takes extra fields for easier authentication"""
    POSITION_CHOICES = (
        (BACKEND_DEVELOPER, _(BACKEND_DEVELOPER)),
        (FRONTEND_DEVEOPER, _(FRONTEND_DEVEOPER)),
        (MOBILE_DEVELOPER, _( MOBILE_DEVELOPER)),
        (PRODUCT_MANAGER, _( PRODUCT_MANAGER)),
    )


    first_name = models.CharField(max_length=30, null=False, blank=False)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=19, unique=True, blank=True)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True, null=True)
    profile_picture = models.ImageField(upload_to="images/user_profile_picture", default="pi.png",
                                validators=[validate_image_size, validate_image_file_extension])
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(validators=[validate_date_of_birth], null=True)
    last_login = models.DateTimeField(auto_now=True)
    permission_level = models.ManyToManyField(PermissionLevel)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]
    objects = UserManager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    class Meta:
        ordering =  ['-date_joined']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def admin_status(self):
        if self.is_superadmin:
            return "Admin"
        return ''
    
    def get_short_name(self):
        return self.first_name[0] + self.last_name[0]
    
    
    @property
    def image_URL(self):
        try:
            url = self.profile_picture.url
        except AttributeError:
            url = ''
        return url
