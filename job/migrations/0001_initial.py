# Generated by Django 4.2.2 on 2023-07-06 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import job.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Job",
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
                ("role", models.CharField(max_length=100)),
                (
                    "skill_level",
                    models.CharField(
                        choices=[
                            ("Junior", "Junior"),
                            ("Senior", "Senior"),
                            ("Mid-level", "Mid-level"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "job_type",
                    models.CharField(
                        choices=[
                            ("On-site", "On-site"),
                            ("Remote", "Remote"),
                            ("Hybrid", "Hybrid"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "job_schedule",
                    models.CharField(
                        choices=[
                            ("Full-time", "Full-time"),
                            ("Project-based", "Project-based"),
                        ],
                        max_length=20,
                    ),
                ),
                ("job_requirements", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
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
                ("name", models.CharField(max_length=200)),
                ("address", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="JobApplication",
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
                ("cover_letter", models.TextField()),
                (
                    "resume",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="resumes/",
                        validators=[job.models.validate_pdf_file],
                    ),
                ),
                ("applied_at", models.DateTimeField(auto_now_add=True)),
                ("is_shortlisted", models.BooleanField(default=False)),
                ("is_invited_for_assessment", models.BooleanField(default=False)),
                ("is_invited_for_interview", models.BooleanField(default=False)),
                ("is_hired", models.BooleanField(default=False)),
                ("is_rejected", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "applicant",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "job",
                    models.ManyToManyField(related_name="applications", to="job.job"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="job",
            name="location",
            field=models.ManyToManyField(
                related_name="job_locations", to="job.location"
            ),
        ),
        migrations.AddField(
            model_name="job",
            name="posted_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
