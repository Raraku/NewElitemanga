# Generated by Django 2.2.6 on 2020-04-21 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20200421_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='tags_string',
            field=models.TextField(blank=True, null=True),
        ),
    ]
