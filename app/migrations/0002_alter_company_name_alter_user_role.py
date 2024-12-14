# Generated by Django 5.1.2 on 2024-12-09 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("Company User", "Company User"),
                    ("Company Admin", "Company Admin"),
                    ("System Admin", "System Admin"),
                ],
                default="User",
                max_length=30,
            ),
        ),
    ]