# Generated by Django 4.2.2 on 2023-07-05 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("job", "0003_location_remove_job_location_job_location"),
    ]

    operations = [
        migrations.RenameField(model_name="job", old_name="title", new_name="role",),
    ]
