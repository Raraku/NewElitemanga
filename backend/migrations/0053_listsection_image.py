# Generated by Django 2.2.6 on 2020-09-05 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0052_auto_20200831_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='listsection',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='list-images'),
        ),
    ]
