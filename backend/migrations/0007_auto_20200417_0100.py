# Generated by Django 2.2.6 on 2020-04-17 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_media_weekly_reads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='pre_image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
