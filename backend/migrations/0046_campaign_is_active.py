# Generated by Django 2.2.6 on 2020-08-16 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0045_auto_20200815_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
