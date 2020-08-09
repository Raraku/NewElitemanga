from django.contrib import admin
from backend.admin import *
from .models import Profile

# Register your models here.
admin.site.register(Profile)
