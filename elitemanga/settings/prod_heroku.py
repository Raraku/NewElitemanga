"""Use this for production"""

from .base import *
import django_heroku
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api


DEBUG = False
ALLOWED_HOSTS += [
    "elitemanga-test.herokuapp.com",
    "https://elitemanga-test.herokuapp.com",
    "https://www.elitemanga-test.herokuapp.com",
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
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost:5000",
    "https://localhost:8000",
    "http://localhost:8000",
    "https://djreact.netlify.com",
    "http://djreact.netlify.com",
    "http://192.168.43.127:3000",
    "http://192.168.43.127",
    "http://192.168.43.127:8000",
    "elitemanga.net",
    "https://elitemanga.net",
    "https://www.elitemanga.net",
    "www.elitemanga.net",
]

CSRF_TRUSTED_ORIGINS = [
    "djreact.netlify.com",
    "http://192.168.43.127:3000",
    "http://192.168.43.127:8000",
    "http://192.168.43.127",
    "http://localhost:3000",
    "localhost:3000",
    "elitemanga.net",
    "https://elitemanga.net",
    "https://www.elitemanga.net",
    "www.elitemanga.net",
]
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "elitemanga",
    "API_KEY": "113342832684136",
    "API_SECRET": "IZU9GTfQCpYWhHXe09YiQEW6SeA",
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
django_heroku.settings(locals(), logging=False, staticfiles=False)
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "elitemangaa@gmail.com"
EMAIL_HOST_PASSWORD = "DaemonicAura01"
EMAIL_PORT = 587
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = True
