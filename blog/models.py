from django.db import models

# Create your models here.
class Blogpost(models.Model):
    title = models.TextField(max_length=60)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField()
    time_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BlogSection(models.Model):
    order_id = models.IntegerField()
    content = models.TextField()
    image = models.ImageField()
    blogpost = models.ForeignKey(Blogpost, on_delete=models.CASCADE)

    class Meta:
        ordering = ["order_id"]

