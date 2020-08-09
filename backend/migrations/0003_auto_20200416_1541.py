# Generated by Django 2.2.6 on 2020-04-16 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20200414_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='last_updated',
        ),
        migrations.AddField(
            model_name='media',
            name='pre_image_url',
            field=models.URLField(default='http://fake.com/media'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='media',
            name='image_url',
            field=models.ImageField(upload_to='media-images'),
        ),
    ]
