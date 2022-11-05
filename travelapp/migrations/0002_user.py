# Generated by Django 4.1.3 on 2022-11-05 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("travelapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("password", models.TextField(default="", max_length=15, unique=True)),
                ("email", models.CharField(max_length=255, unique=True)),
                ("travel_type", models.CharField(max_length=255, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={"db_table": "user",},
        ),
    ]
