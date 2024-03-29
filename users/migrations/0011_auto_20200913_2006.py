# Generated by Django 2.2.6 on 2020-09-13 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200905_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='profile-avatars/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='product-thumbnails/'),
        ),
    ]
