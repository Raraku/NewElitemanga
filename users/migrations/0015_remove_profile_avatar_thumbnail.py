# Generated by Django 2.2.6 on 2020-09-15 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20200913_2355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar_thumbnail',
        ),
    ]
