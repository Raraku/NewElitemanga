from django.db import models
from django.core.files import File
from urllib.request import urlopen
import urllib3
from tempfile import NamedTemporaryFile
from django.utils.translation import ugettext_lazy as _
import json
import requests
from elitemanga.settings.base import AUTH_USER_MODEL, BASE_DIR
from django.contrib.sessions.models import Session
from django.contrib.postgres.fields import JSONField
from users.models import Profile
from django.utils.timezone import make_aware
from taggit.managers import TaggableManager
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager
from taggit.models import ItemBase, TagBase
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary import CloudinaryResource
import cloudinary.uploader


class MyCustomTag(TagBase):
    # ... fields here

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name

    # ... methods (if any) here


class ListTaggedItemBase(ItemBase):
    tag = models.ForeignKey(
        MyCustomTag,
        related_name="%(app_label)s_%(class)s_items",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class TaggedList(ListTaggedItemBase):
    content_object = models.ForeignKey("List", on_delete=models.CASCADE)


# Create your models here.


class Source(models.Model):
    # SOURCE = (
    #     ("1", "Webtoons"),
    #     ("2", "Crunchyroll"),
    #     ("3", "Mangakakalot"),
    #     ("4", "anime-planet"),
    #     ("5", "Animepahe"),
    #     ("6", "Netflix"),
    #     ("7", "Toomics"),
    # )
    official = models.BooleanField()
    name = models.CharField(max_length=50)
    homepage = models.URLField()
    # type = models.CharField(choices=SOURCE, max_length=40)
    # image = CloudinaryField("image")
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Media(models.Model):
    RANK = (("1", "Kami"), ("2", "S"), ("3", "A"),
            ("4", "B"), ("5", "Unranked"))
    MEDIA_STATUS = (
        ("0", "Finished"),
        ("1", "Ongoing"),
        ("2", "Unreleased"),
        ("3", "Upcoming"),
    )
    MEDIA_TYPE = (("0", "Manga"), ("1", "Anime"))
    chapters_length = models.IntegerField(default=0)
    author = models.CharField(max_length=70)
    title = models.TextField(max_length=200)
    description = models.TextField()
    hits = models.IntegerField()
    other_names = models.TextField(blank=True)
    alias = models.TextField(max_length=80, unique=False)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=MEDIA_STATUS, max_length=32)
    pre_image_url = models.URLField(blank=True, null=True)
    # image_url = models.URLField(blank=True, null=True)
    # image_url = models.ImageField(
    #     # upload_to="media-images/",
    #     blank=True, null=True)
    image_url = CloudinaryField("image", blank=True, null=True)
    rank = models.CharField(max_length=32, choices=RANK, default=RANK[4][0])
    baka = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, default="", blank=True, null=True)
    tags_string = models.TextField(blank=True, null=True)
    reviewed = models.BooleanField(default=False)
    sources = models.ManyToManyField(Source, through="SourceLink", blank=True)
    # either to leave the url here or to access it through the through model, unable to decide.
    publisher_url = models.URLField(blank=True, null=True)
    publisher_url_2 = models.URLField(blank=True, null=True)
    scanlator_1 = models.URLField(blank=True, null=True)
    scanlator_2 = models.URLField(blank=True, null=True)
    media_type = models.CharField(max_length=32, choices=MEDIA_TYPE)
    tags = TaggableManager()
    adaptation = models.OneToOneField(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    weekly_reads = models.IntegerField(default=0)

    class Meta:
        ordering = ["-hits"]

    def __str__(self):
        return self.title + " " + str(self.media_type)

    def save(self, *args, **kwargs):
        if self.pre_image_url and self.image_url:
            print("working " + self.title)
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
            }
            img_temp = NamedTemporaryFile(delete=True)
            req = requests.get(self.pre_image_url, headers=headers)
            img_temp.write(req.content)
            img_temp.flush()
            image = Image.open(img_temp)
            image = image.convert("RGB")
            temp_thumb = BytesIO()
            image.save(temp_thumb, "PNG")
            temp_thumb.seek(0)
            # set save=False, otherwise it'll run in an infinite loop
            data = cloudinary.uploader.upload(ContentFile(temp_thumb.read()), public_id=str(
                self.title + str(self.media_type)), resource_type="image", folder="media/media-images/")
            self.image_url = CloudinaryResource(public_id=data.get(
                "public_id"), format=data.get("format"), signature=data.get("signature"), version=data.get("version"), type="upload", resource_type=data.get("resource_type"), metadata=data)
            # self.image_url = self.alias + \
            #     ".png", ContentFile(temp_thumb.read())
            # self.image_url.save(
            #     self.alias + ".png", ContentFile(temp_thumb.read()), save=False
            # )
            temp_thumb.close()
        super(Media, self).save(*args, **kwargs)


class SourceLink(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    link = models.URLField()


class List(models.Model):
    title = models.CharField(max_length=256)
    upvotes = models.IntegerField()
    tags = TaggableManager(through=TaggedList)
    image = models.ImageField(
        # upload_to="list-images/",
        blank=True, null=True, default="list-images/p.png"
    )
    # image = CloudinaryField("image", blank=True, null=True)
    intro = models.TextField()
    slug = models.SlugField(max_length=200, default="")
    date_uploaded = models.DateTimeField(auto_now_add=True)


class ListSection(models.Model):
    media = models.ForeignKey(to=Media, on_delete=models.SET_NULL, null=True)
    list = models.ForeignKey(to=List, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    # image = CloudinaryField("image", blank=True, null=True)
    image = models.ImageField(
        # upload_to="list-images",
        blank=True, null=True)
    position = models.IntegerField()

    def __str__(self):
        return self.media.title + " No: " + str(self.position)


class ElitemangaReview(models.Model):
    moment = models.TextField(
        blank=True,
        null=True,
        default="<p><b>Presentation:</b></p><p><b>Consistency:</b></p><p><b>Predictability:</b></p><p><b>Effort:</b></p><p><b>Main Genre of Moments:</b></p><p><b><br></b></p>",
    )
    moment_score = models.IntegerField(
        default=0, validators=[(MinValueValidator(0)), MaxValueValidator(10)]
    )
    plot = models.TextField(
        blank=True,
        null=True,
        default='<p><span style="font-weight: 700;">Realism:</span></p><p><span style="font-weight: 700;">Premise:</span></p><p><span style="font-weight: 700;">Pacing:</span></p><p><span style="font-weight: 700;">Complexity:</span></p><p><span style="font-weight: 700;">Immersion:</span></p><p><span style="font-weight: 700;">Conclusion:</span></p>',
    )
    plot_score = models.IntegerField(
        default=0, validators=[(MinValueValidator(0)), MaxValueValidator(10)]
    )
    characters = models.TextField(
        blank=True,
        null=True,
        default="<p><b>Personality:</b></p><p><b>Chemistry:</b></p><p><b>Backdrop:</b></p><p><b>Likability:</b></p><p><b>Development:</b></p>",
    )
    characters_score = models.IntegerField(
        default=0, validators=[(MinValueValidator(0)), MaxValueValidator(10)]
    )
    quality = models.TextField(
        blank=True,
        null=True,
        default="<p><b>Sound:</b></p><p><b>Voice Acting:</b></p><p><b>Art style:</b></p><p><b>Animation Quality:</b></p>",
    )
    quality_score = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    remark = models.TextField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    media_review = models.OneToOneField(
        to=Media, on_delete=models.CASCADE, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        self.total_score = (
            self.moment_score
            + self.plot_score
            + self.characters_score
            + self.quality_score
        )
        super(ElitemangaReview, self).save(*args, **kwargs)


class Review(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    media = models.ForeignKey(
        Media, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    created = models.DateField(auto_now_add=True)
    moment_score = models.IntegerField(default=0)
    plot_score = models.IntegerField(default=0)
    characters_score = models.IntegerField(default=0)
    quality_score = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created"]


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ["-created"]


class ReviewVote(models.Model):
    CHOICES = (("1", "Like"), ("2", "Dislike"))
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice = models.CharField(choices=CHOICES, max_length=32)
    user_review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="review_vote"
    )


# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=70)
    content = models.TextField()
    date_written = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default="", max_length=150)

    def __str__(self):
        return self.title


class Campaign(models.Model):
    title = models.CharField(max_length=70)
    is_active = models.BooleanField(default=False)


class Referral(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    referrals = models.ManyToManyField(
        Profile, related_name="referred", blank=True, related_query_name="referred"
    )
