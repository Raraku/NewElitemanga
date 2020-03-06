from django.contrib import admin
from .models import Manga, UserManga, MangaTag, Chapter
from users.models import User
from django.contrib.sessions.models import Session


# Register your models here.


class ChapterInline(admin.TabularInline):
    model = Chapter


class UserChapterInline(admin.TabularInline):
    model = UserManga.chapters.through


class MangaAdmin(admin.ModelAdmin):
    list_display = ("title", "last_updated", "rank", "hits")
    list_filter = ("rank", "last_updated", "tags", "author", "title", "manga_type")
    filter_horizontal = ("tags",)
    search_fields = ("title", "keywords")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        ChapterInline,
    ]


class UserMangaAdmin(admin.ModelAdmin):
    list_display = ("user", "manga", "last_read")
    list_filter = ("user", "last_read")
    search_fields = ("manga",)
    inlines = [UserChapterInline]
    exclude = ("chapters",)


admin.site.register(Session)
admin.site.register(User)
admin.site.register(Manga, MangaAdmin)
admin.site.register(UserManga, UserMangaAdmin)
admin.site.register(MangaTag)
