# Generated by Django 2.2.6 on 2020-04-21 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_media_reviewed'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElitemangaReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('originality', models.TextField()),
                ('originality_score', models.IntegerField(default=0)),
                ('plot', models.TextField()),
                ('plot_score', models.IntegerField(default=0)),
                ('characters', models.TextField()),
                ('characters_score', models.IntegerField(default=0)),
                ('quality', models.TextField()),
                ('quality_score', models.IntegerField(default=0)),
                ('remark', models.TextField()),
                ('total_score', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='media',
            name='rank_reason',
        ),
        migrations.RemoveField(
            model_name='media',
            name='thoughts',
        ),
        migrations.AddField(
            model_name='media',
            name='unreleased',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='media',
            name='elitemanga_review',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ElitemangaReview'),
        ),
    ]
