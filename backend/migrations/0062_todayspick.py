# Generated by Django 2.2.6 on 2022-02-07 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0061_auto_20200921_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodaysPick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backend.Media')),
            ],
        ),
    ]
