# Generated by Django 2.2.6 on 2020-06-19 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0029_auto_20200617_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='alias',
            field=models.TextField(max_length=80),
        ),
    ]