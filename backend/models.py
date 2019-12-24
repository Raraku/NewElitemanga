from django.db import models
from django.contrib.auth.models import AnonymousUser
import json
import requests
from elitemanga.settings.base import AUTH_USER_MODEL, BASE_DIR

# Create your models here.

class MangaTag(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class MangaManager(models.Manager):
    def create_manga(self, name, alias, date_added, last_updated, url, rank, tags):
        with open(BASE_DIR + '/mangaid.json', 'r') as target:
            data = json.load(target)
            query =  data[alias]
            response = requests.get(f'https://www.mangaeden.com/api/manga/{query}/')
            response = response.json()
            return(query)
        
        manga = self.create(name=name, date_added=date, last_updated=last_updated, url=url, rank=rank, tags=tags)
        return manga

class Manga(models.Model):
    RANK = (
        ('1', 'Kami'),
        ('2', 'S'),
        ('3', 'A'),
        ('4', 'B'),
        ('5', 'Unranked')
        )
    name = models.TextField(max_length=200, unique=True)
    alias = models.TextField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField()
    url = models.URLField()
    rank = models.CharField(max_length=32, choices =RANK , default=RANK[4] )
    tags = models.ManyToManyField(MangaTag, blank=True)
    slug = models.SlugField(max_length=200, default='')

    def __str__(self):
        return self.alias

class Chapter(models.Model):
    url = models.URLField()
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)



class UserManga(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    last_read = models.DateTimeField(blank=True)

    def __str__(self):
        return self.manga.name

class UserChapter(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    manga = models.ForeignKey(UserManga, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

class Favorites(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    mangas = models.ForeignKey(UserManga, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.name + ' ' + self.mangas.name
    
