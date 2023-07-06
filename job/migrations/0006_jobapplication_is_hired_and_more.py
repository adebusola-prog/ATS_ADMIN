# Generated by Django 4.2.2 on 2023-07-06 03:23

from django.db import migrations, models
import job.models


class Migration(migrations.Migration):

    dependencies = [
        ("job", "0005_job_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplication",
            name="is_hired",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="is_invited_for_assessment",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="is_invited_for_interview",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="is_rejected",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="is_shortlisted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="resume",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="resumes/",
                validators=[job.models.validate_pdf_file],
            ),
        ),
        migrations.RemoveField(model_name="jobapplication", name="job",),
        migrations.AddField(
            model_name="jobapplication",
            name="job",
            field=models.ManyToManyField(related_name="applications", to="job.job"),
        ),
    ]
