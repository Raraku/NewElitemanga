# Generated by Django 2.2.6 on 2020-07-31 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0037_auto_20200731_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='slug',
            field=models.SlugField(default='fake'),
            preserve_default=False,
        ),
    ]
