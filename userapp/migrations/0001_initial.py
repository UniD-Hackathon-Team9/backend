# Generated by Django 4.1.3 on 2022-11-05 18:57

from django.db import migrations, models
import userapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=50)),
                ('person_type', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E')], max_length=2, null=True)),
                ('select_view', models.BooleanField(null=True)),
                ('select_cafe', models.BooleanField(null=True)),
                ('select_drink', models.BooleanField(null=True)),
                ('select_food', models.BooleanField(null=True)),
                ('select_activity', models.BooleanField(null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', userapp.models.UserManager()),
            ],
        ),
    ]
