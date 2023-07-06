# Generated by Django 4.2.2 on 2023-07-05 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_customuser_profile_picture"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser", options={"ordering": ["date_joined"]},
        ),
        migrations.AlterField(
            model_name="customuser",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="permission_level",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Content_manager", "Content Manager"),
                    ("Membership_manager", "Membership Manager"),
                    ("Assessment_manager", "Assessment Manager"),
                    ("Application_manager", "Application Manager"),
                    ("Superadmin", "Super Admin"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="position",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Backend_developer", "Backend Developer"),
                    ("Frontend_developer", "Frontend Developer"),
                    ("Mobile_developer", "Mobile Developer"),
                    ("Product_Manager", "Product Manager"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
