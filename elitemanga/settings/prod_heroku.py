"""Use this for production"""

from .base import *
import django_heroku
import dj_database_url

DEBUG = False
ALLOWED_HOSTS += [
    "elitemanga-test.herokuapp.com",
]
WSGI_APPLICATION = "elitemanga.wsgi.application"

DATABASES = {}
DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)

CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "build", "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "build", "media")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
django_heroku.settings(locals())
