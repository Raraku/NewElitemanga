# Generated by Django 2.2.6 on 2020-06-03 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_auto_20200602_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='list',
            name='image',
            field=models.ImageField(blank=True, default='list-images/p.png', null=True, upload_to='list-images'),
        ),
    ]
