# Generated by Django 2.2.6 on 2020-08-15 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_is_referred'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_referred',
        ),
    ]
