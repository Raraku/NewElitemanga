# Generated by Django 2.2.6 on 2020-05-09 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_auto_20200509_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='total_score',
        ),
    ]
