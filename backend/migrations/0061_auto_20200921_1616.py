# Generated by Django 2.2.6 on 2020-09-21 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0060_auto_20200918_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elitemangareview',
            old_name='moment',
            new_name='entertainment_value',
        ),
        migrations.RenameField(
            model_name='elitemangareview',
            old_name='moment_score',
            new_name='entertainment_value_score',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='moment_score',
            new_name='entertainment_value_score',
        ),
    ]
