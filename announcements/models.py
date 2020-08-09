from django.db import models

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=70)
    content = models.TextField()
    uploaded_on = models.DateTimeField(auto_now_add=True)

