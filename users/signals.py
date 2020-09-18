from django.db.models.signals import post_save, pre_save
from elitemanga.settings.base import AUTH_USER_MODEL
from django.dispatch import receiver
from .models import Profile
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from functools import wraps
import requests
from cloudinary import CloudinaryResource
import cloudinary.uploader
from tempfile import NamedTemporaryFile

THUMBNAIL_SIZE = (100, 100)


def disable_for_loaddata(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs["raw"]:
            print("Skipping signal for %s %s" % (args, kwargs))
            return
        signal_handler(*args, **kwargs)

    return wrapper


@disable_for_loaddata
@receiver(post_save, sender=AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance, username=instance.username)


@disable_for_loaddata
@receiver(post_save, sender=AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    if kwargs.get("raw", False):
        return False
    instance.profile.save()


# @disable_for_loaddata
# @receiver(pre_save, sender=Profile)
# def generate_thumbnail(sender, instance, **kwargs):
#     if kwargs.get("raw", False):
#         return False
#     if instance.avatar:
#         headers = {
#             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
#         }
#         img_temp = NamedTemporaryFile(delete=True)
#         print(instance.avatar.url)
#         req = requests.get(instance.avatar.url, headers=headers)
#         img_temp.write(req.content)
#         img_temp.flush()
#         image = Image.open(img_temp)
#         image = image.convert("RGB")
#         image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

#         temp_thumb = BytesIO()
#         image.save(temp_thumb, "PNG")
#         temp_thumb.seek(0)
#         # set save=False, otherwise it'll run in an infinite loop
#         # instance.avatar_thumbnail.save(
#         #     instance.avatar.name, ContentFile(temp_thumb.read()), save=False
#         # )
#         data = cloudinary.uploader.upload(ContentFile(
#             temp_thumb.read()), public_id=str(instance.username[:15], resource_type="image", folder="media/product-thumbnails/")
#         instance.avatar_thumbnail=CloudinaryResource(public_id=data.get(
#             "public_id"), format=data.get("format"), signature=data.get("signature"), version=data.get("version"), type="upload", resource_type=data.get("resource_type"), metadata=data)
#         temp_thumb.close()
#         instance.save()

# Original
# @disable_for_loaddata
# @receiver(pre_save, sender=Profile)
# def generate_thumbnail(sender, instance, **kwargs):
#     if kwargs.get("raw", False):
#         return False
#     if instance.avatar:
#         image = Image.open(instance.avatar)
#         image = image.convert("RGB")
#         image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

#         temp_thumb = BytesIO()
#         image.save(temp_thumb, "PNG")
#         temp_thumb.seek(0)
#         # set save=False, otherwise it'll run in an infinite loop
#         instance.avatar_thumbnail.save(
#             instance.avatar.name, ContentFile(temp_thumb.read()), save=False
#         )
#         temp_thumb.close()
