# Generated by Django 2.2.6 on 2020-04-14 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0001_initial'),
        ('users', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewvote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reviewvote',
            name='user_review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_vote', to='backend.Review'),
        ),
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
        migrations.AddField(
            model_name='review',
            name='media',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Media'),
        ),
        migrations.AddField(
            model_name='media',
            name='publisher',
            field=models.ManyToManyField(blank=True, to='backend.Publisher'),
        ),
        migrations.AddField(
            model_name='media',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Review'),
        ),
    ]
