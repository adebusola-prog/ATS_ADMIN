# Generated by Django 4.2.2 on 2023-07-14 13:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("job", "0007_alter_jobapplication_applicant_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="jobapplication", unique_together={("job", "applicant")},
        ),
    ]