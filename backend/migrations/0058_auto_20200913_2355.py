# Generated by Django 2.2.6 on 2020-09-13 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0057_auto_20200913_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='image',
            field=models.ImageField(blank=True, default='list-images/p.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='listsection',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='media',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
