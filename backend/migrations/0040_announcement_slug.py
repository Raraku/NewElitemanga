# Generated by Django 2.2.6 on 2020-07-31 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0039_remove_announcement_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='slug',
            field=models.SlugField(default='none', max_length=150),
        ),
    ]