# Generated by Django 2.2.6 on 2020-07-31 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0035_auto_20200630_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('content', models.TextField()),
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
