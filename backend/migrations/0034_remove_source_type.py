# Generated by Django 2.2.6 on 2020-06-30 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0033_auto_20200629_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='type',
        ),
    ]