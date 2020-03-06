"""Use this for production"""

from .base import *

DEBUG = False
ALLOWED_HOSTS += [
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
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_USER = "username"
EMAIL_HOST = "smtp.domain.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = "password"

