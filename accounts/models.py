from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from .validators import validate_image_size
from django.core.validators import validate_image_file_extension

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, gender, password=None):
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(username=username, first_name=first_name,
                          last_name=last_name, email=self.normalize_email(email))
        # user.password = make_password(password)
        user.set_password(password)
        user.gender = gender
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password, gender=None):
        existing_superadmin = self.filter(permission_level='superadmin').exists()
        if existing_superadmin:
            raise ValueError("Only one user can have the 'superadmin' permission level.")
        user = self.create_user(first_name=first_name, last_name=last_name, gender=gender or None,
                                username=username, email=self.normalize_email(email), password=password)
        
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.permission_level = 'superadmin'
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    """Custom User Model that takes extra fields for easier authentication"""

    PERMISSION_LEVEL_CHOICES = (
        ('content_manager', _('Content Manager')),
        ('membership_manager', _('Membership Manager')),
        ('assessment_manager', _('Assessment Manager')),
        ('application_manager', _('Application Manager')),
        ('superadmin', _('Super Admin')),
    )

    POSITION_CHOICES = (
        ('backend_developer', _('Backend Developer')),
        ('frontend_developer', _('Frontend Developer')),
        ('mobile_developer', _('Mobile Developer')),
        ('product_designer', _('Product Designer')),
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
    last_login = models.DateTimeField(auto_now=True)
    permission_level = models.CharField(max_length=20, choices=PERMISSION_LEVEL_CHOICES, blank=True, null=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]
    objects = UserManager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    class Meta:
        ordering =  ['date_joined']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def admin_status(self):
        if self.is_superadmin:
            return "Admin"
        return ''
    
    
    @property
    def image_URL(self):
        try:
            url = self.profile_picture.url
        except AttributeError:
            url = ''
        return url
