"""Use this for production"""
from google.oauth2 import service_account
from .base import *

# gOOGLE CLOUD STORAGE SETTINGS
DEFAULT_FILE_STORAGE = "elitemanga.settings.gcloud.GoogleCloudMediaFileStorage"
STATICFILES_STORAGE = "elitemanga.settings.gcloud.GoogleCloudStaticFileStorage"
GS_PROJECT_ID = "elitemanga-79e49"
GS_STATIC_BUCKET_NAME = "elitemanga-data"
GS_MEDIA_BUCKET_NAME = "elitemanga-data"  # same as STATIC BUCKET if using single bucket both for static and media
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, "Elitemanga-684ea95a36f1.json")
)
STATIC_URL = "https://storage.googleapis.com/{}/static/".format(GS_STATIC_BUCKET_NAME)
STATIC_ROOT = "static/"

MEDIA_URL = "https://storage.googleapis.com/{}/media/".format(GS_MEDIA_BUCKET_NAME)
MEDIA_ROOT = "media/"


DEBUG = False
ALLOWED_HOSTS += [
    "api.elitemanga.net",
    "https://elitemanga.net",
    "http://elitemanga.net",
    "https://elitemangas.com",
    "https://elitemanga-79e49.appspot.com",
    "http://elitemanga-79e49.appspot.com",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "/cloudsql/elitemanga-79e49:us-central1:nga-79e49:us-central1:elitemanga-database-01",
        "USER": "postgres",
        "PASSWORD": "godisgood",
        "HOST": "elitemanga-database",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
]


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_USER = "username"
EMAIL_HOST = "smtp.domain.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = "password"
