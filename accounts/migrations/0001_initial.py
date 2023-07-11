# Generated by Django 4.2.2 on 2023-07-11 09:03

import accounts.models
import accounts.validators
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="PermissionLevel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("first_name", models.CharField(max_length=30)),
                ("middle_name", models.CharField(blank=True, max_length=30, null=True)),
                ("username", models.CharField(blank=True, max_length=19, unique=True)),
                ("last_name", models.CharField(max_length=30)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, null=True, region=None, unique=True
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        default="pi.png",
                        upload_to="images/user_profile_picture",
                        validators=[
                            accounts.validators.validate_image_size,
                            django.core.validators.validate_image_file_extension,
                        ],
                    ),
                ),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "date_of_birth",
                    models.DateField(
                        null=True, validators=[accounts.models.validate_date_of_birth]
                    ),
                ),
                ("last_login", models.DateTimeField(auto_now=True)),
                (
                    "position",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Backend Developer", "Backend Developer"),
                            ("Frontend Developer", "Frontend Developer"),
                            ("Mobile Developer", "Mobile Developer"),
                            ("Product Manager", "Product Manager"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_superadmin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "permission_level",
                    models.ManyToManyField(to="accounts.permissionlevel"),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"ordering": ["-date_joined"],},
            managers=[("objects", django.contrib.auth.models.UserManager()),],
        ),
    ]
