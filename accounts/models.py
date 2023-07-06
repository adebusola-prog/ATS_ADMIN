from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from .validators import validate_image_size
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError
from datetime import date
from base import constants
from base.managers import ActiveManager, InActiveManager

def validate_date_of_birth(value):
    if value.year > date.today().year:
        raise ValidationError("Date of birth cannot be in the future.")
    

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(username=username, first_name=first_name,
                          last_name=last_name, email=self.normalize_email(email))
    
        user.set_password(password)
        user.save(using=self._db)
        return user
       
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(first_name=first_name, last_name=last_name,
                                username=username, email=self.normalize_email(email), password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.save(using=self._db)

        return user

class PermissionLevel(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    """Custom User Model that takes extra fields for easier authentication"""
    
    BACKEND_DEVELOPER = constants.BACKEND_DEVELOPER
    FRONTEND_DEVEOPER = constants.FRONTEND_DEVEOPER
    MOBILE_DEVELOPER = constants.MOBILE_DEVELOPER 
    PRODUCT_MANAGER = constants.PRODUCT_MANAGER
   

    POSITION_CHOICES = (
        ('Backend_developer', _(BACKEND_DEVELOPER)),
        ('Frontend_developer', _(FRONTEND_DEVEOPER)),
        ('Mobile_developer', _( MOBILE_DEVELOPER )),
        ('Product_Manager', _( PRODUCT_MANAGER)),
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
