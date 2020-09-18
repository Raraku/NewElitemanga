from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
import requests
from cloudinary import CloudinaryResource
import cloudinary.uploader
from tempfile import NamedTemporaryFile

# Create your models here.


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("You must provide an email")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(("email address"), blank=False, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserAccountManager()

    def __str__(self):
        if self.first_name != "":
            return self.first_name + " " + self.last_name
        else:
            return self.username


THUMBNAIL_SIZE = (100, 100)


class Profile(models.Model):
    LEVELS = (("0", "Initiate"),)
    username = models.CharField(max_length=80, unique=True)
    level = models.CharField(
        max_length=80, choices=LEVELS, default=LEVELS[0][0])
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # avatar = models.ImageField(
    #     blank=True, null=True,
    #     # upload_to="profile-avatars/"
    # )
    avatar = CloudinaryField("image", blank=True, null=True)
    # avatar_thumbnail = models.ImageField(
    #     # upload_to="product-thumbnails/",
    #     null=True, blank=True,
    # )
    avatar_thumbnail = CloudinaryField("image", blank=True, null=True)
    social_avatar = models.URLField(blank=True, null=True)
    is_referred = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s profile"

    # def check_level(self):
    #     profile = self.get_object()
    #     highest=profile.user.review_set.order_by('-likes')[0]
    #     if highest.likes > 100 < 200:
    #         self.level
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.username))
        if self.avatar:
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
            }
            img_temp = NamedTemporaryFile(delete=True)
            print(self.avatar.url)
            req = requests.get(self.avatar.url, headers=headers)
            img_temp.write(req.content)
            img_temp.flush()
            image = Image.open(img_temp)
            image = image.convert("RGB")
            image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

            temp_thumb = BytesIO()
            image.save(temp_thumb, "PNG")
            temp_thumb.seek(0)
            # set save=False, otherwise it'll run in an infinite loop
            # instance.avatar_thumbnail.save(
            #     instance.avatar.name, ContentFile(temp_thumb.read()), save=False
            # )
            data = cloudinary.uploader.upload(ContentFile(
                temp_thumb.read()), resource_type="image", folder="media/product-thumbnails/")
            self.avatar_thumbnail = CloudinaryResource(public_id=data.get(
                "public_id"), format=data.get("format"), signature=data.get("signature"), version=data.get("version"), type="upload", resource_type=data.get("resource_type"), metadata=data)
            temp_thumb.close()
        super(Profile, self).save(*args, **kwargs)
