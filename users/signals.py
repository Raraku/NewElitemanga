from django.db.models.signals import post_save, pre_save
from elitemanga.settings.base import AUTH_USER_MODEL
from django.dispatch import receiver
from .models import Profile
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

THUMBNAIL_SIZE = (50, 50)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_save, sender=Profile)
def generate_thumbnail(sender, instance, **kwargs):
    if instance.avatar:
        image = Image.open(instance.avatar)
        image = image.convert("RGB")
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_thumb = BytesIO()
        image.save(temp_thumb, "PNG")
        temp_thumb.seek(0)
        # set save=False, otherwise it'll run in an infinite loop
        instance.avatar_thumbnail.save(
            instance.avatar.name, ContentFile(temp_thumb.read()), save=False
        )
        temp_thumb.close()
