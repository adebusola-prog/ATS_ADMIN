# Generated by Django 4.2.2 on 2023-07-11 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ActivityLog",
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
                (
                    "action_type",
                    models.CharField(
                        choices=[
                            ("Create", "Create"),
                            ("Read", "Read"),
                            ("Update", "Update"),
                            ("Delete", "Delete"),
                            ("Login", "Login"),
                            ("Logout", "Logout"),
                            ("Login Failed", "Login Failed"),
                        ],
                        max_length=15,
                    ),
                ),
                ("action_time", models.DateTimeField(auto_now_add=True)),
                ("remarks", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("Success", "Success"), ("Failed", "Failed")],
                        default="Success",
                        max_length=7,
                    ),
                ),
                ("data", models.JSONField(default=dict)),
                ("object_id", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "actor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
    ]
