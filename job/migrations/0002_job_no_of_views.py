# Generated by Django 4.2.2 on 2023-07-09 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="no_of_views",
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
