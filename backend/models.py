from django.db import models
import json
import requests
from elitemanga.settings.base import AUTH_USER_MODEL, BASE_DIR
from django.contrib.sessions.models import Session
from django.contrib.postgres.fields import JSONField

from django.utils.timezone import make_aware

# Create your models here.


class MangaTag(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    title = models.CharField(max_length=48)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Manga(models.Model):
    RANK = (("1", "Kami"), ("2", "S"), ("3", "A"), ("4", "B"), ("5", "Unranked"))
    MANGA_STATUS = (("0", "Finished"), ("1", "Ongoing"))
    MANGA_TYPE = (("0", "MANGANELO"),)
    manga_type = models.CharField(choices=MANGA_TYPE, max_length=32)
    chapters_length = models.IntegerField(default=0)
    author = models.CharField(max_length=70)
    last_updated = models.DateTimeField()
    title = models.TextField(max_length=200)
    description = models.TextField()
    hits = models.IntegerField()
    other_names = models.TextField(blank=True)
    alias = models.TextField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=MANGA_STATUS, max_length=32)
    image_url = models.URLField()
    rank = models.CharField(max_length=32, choices=RANK, default=RANK[4])
    baka = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, default="", blank=True, null=True)
    tags = models.ManyToManyField(MangaTag, blank=True)
    tags_string = models.TextField()
    thoughts = models.TextField(blank=True, null=True)
    rank_reason = models.TextField(blank=True, null=True)
    publisher = models.ManyToManyField(Publisher, blank=True)
    publisher_url = models.URLField(blank=True, null=True)
    publisher_url_2 = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["last_updated"]

    def __str__(self):
        return self.alias


class Chapter(models.Model):
    CHAPTER_TYPE = (("0", "MANGAEDEN"), ("1", "MANGANELO"))
    number = models.FloatField()
    date_uploaded = models.DateTimeField()
    title = models.CharField(blank=True, null=True, max_length=255)
    pages = JSONField()
    manga = models.ForeignKey(Manga, related_name="chapters", on_delete=models.CASCADE)
    manga_alias = models.CharField(blank=True, null=True, max_length=100)
    chapter_type = models.CharField(choices=CHAPTER_TYPE, max_length=50)

    def __str__(self):
        return self.manga.title + " " + str(self.number)

    class Meta:
        ordering = ["date_uploaded"]


class UserManga(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    anonymous = models.ForeignKey(
        Session, on_delete=models.CASCADE, blank=True, null=True
    )
    last_read = models.DateTimeField(auto_now_add=True)
    alias = models.CharField(max_length=70)
    isfavorite = models.BooleanField(default=False)
    # read chapters added below
    chapters = models.ManyToManyField(Chapter)
    new_chapters = models.ManyToManyField(Chapter, related_name="recent_chapters")

    def __str__(self):
        return self.alias

