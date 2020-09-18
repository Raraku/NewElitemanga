from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

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
        super(Profile, self).save(*args, **kwargs)
