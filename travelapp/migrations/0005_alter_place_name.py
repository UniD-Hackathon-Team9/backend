# Generated by Django 4.1.3 on 2022-11-05 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0004_alter_place_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
