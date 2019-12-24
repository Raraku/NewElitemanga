from django.contrib import admin
from .models import Manga, Favorites, UserManga, MangaTag, Chapter, UserChapter
from main.models import User
# Register your models here.

class ChapterInline(admin.TabularInline):
    model = Chapter

class UserChapterInline(admin.TabularInline):
    model = UserChapter

class MangaAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_updated', 'rank', 'slug')
    list_filter = ('rank', 'last_updated', 'tags')
    filter_horizontal = ('tags',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        ChapterInline,
    ]

class UserMangaAdmin(admin.ModelAdmin):
    list_display = ('user', 'manga', 'last_read')
    list_filter = ('user', 'last_read')
    search_fields = ('manga',)
    inlines = [
        UserChapterInline,
    ]



admin.site.register(User)
admin.site.register(Manga, MangaAdmin)
admin.site.register(UserManga, UserMangaAdmin)
admin.site.register(MangaTag)
admin.site.register(Favorites)
