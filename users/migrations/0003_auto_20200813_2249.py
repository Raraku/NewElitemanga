# Generated by Django 2.2.6 on 2020-08-13 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_date_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar_thumbnail',
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.URLField(blank=True, null=True),
        ),
    ]