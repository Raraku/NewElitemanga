"""Use this for development"""

from .base import *

ALLOWED_HOSTS += ["127.0.0.1", "localhost",
                  "192.168.43.127", "192.168.43.127:8000"]
DEBUG = True

WSGI_APPLICATION = "elitemanga.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "elitemangadatabase",
        "USER": "elitemanga",
        "PASSWORD": "godisgood",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "elitemanga-database",
#         "USER": "postgres",
#         "PASSWORD": "godisgood",
#         "HOST": "127.0.0.1",
#         "PORT": "3306",
#     }
# }
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000000

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
]

CSRF_TRUSTED_ORIGINS = [
    "djreact.netlify.com",
    "http://192.168.43.127:3000",
    "http://192.168.43.127:8000",
    "http://192.168.43.127",
    "http://localhost:3000",
    "localhost:3000",
]

PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "AIzaSyCZphUPPbPM7B3exfrwND5wI-YIeq9j_hU",
}
# tEST EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "airenov500@gmail.com"
EMAIL_HOST_PASSWORD = "IsraelAire"
EMAIL_PORT = 587
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "elitemanga",
    "API_KEY": "113342832684136",
    "API_SECRET": "IZU9GTfQCpYWhHXe09YiQEW6SeA",
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
