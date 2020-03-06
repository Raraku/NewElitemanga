from django.db import models

# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=32)

class Choices(models.Model):
    title = models.CharField(max_length=72)
    description = models.TextField(blank=True, null=True)
    votes = models.IntegerField(default=0)