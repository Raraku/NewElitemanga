from django.contrib import admin
from django import forms
from .models import (
    Media,
    Review,
    Comment,
    ReviewVote,
    ElitemangaReview,
    List,
    ListSection,
    TaggedList,
    MyCustomTag,
    Source,
    SourceLink,
    Announcement,
    Referral,
    Campaign,
)
from admin_ordering.admin import OrderableAdmin
from users.models import User
from django.contrib.sessions.models import Session
from django_summernote.widgets import SummernoteWidget


# Register your models here.


class ListSectionInline(admin.StackedInline):
    ordering = ("position",)
    model = ListSection


class SourceLinkInline(admin.StackedInline):
    model = SourceLink


class TagSectionInline(admin.TabularInline):
    model = TaggedList


class ListAdmin(admin.ModelAdmin):
    list_display = ("title", "date_uploaded", "upvotes")
    exclude = ("tags",)
    inlines = [TagSectionInline, ListSectionInline]

    prepopulated_fields = {"slug": ("title",)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


class ElitemngaReviewInline(admin.StackedInline):
    model = ElitemangaReview

    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        items = ["entertainment_value", "characters", "plot", "quality"]
        if db_field.name in items:
            kwargs["widget"] = SummernoteWidget()
            kwargs.pop("request")
            return db_field.formfield(**kwargs)
        return super(ElitemngaReviewInline, self).formfield_for_dbfield(
            db_field, **kwargs
        )


# class UserChapterInline(admin.TabularInline):
#     model = UserManga.chapters.through


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "date_written")
    list_filter = ("date_written",)
    prepopulated_fields = {"slug": ("title",)}


class MediaAdmin(admin.ModelAdmin):
    list_display = ("title", "rank", "hits", "media_type", "weekly_reads")
    list_filter = ("media_type", "rank", "author", "status", "reviewed")
    search_fields = ("title", "keywords")
    prepopulated_fields = {"slug": ("title",)}
    # inlines = [SourceLinkInline, ElitemngaReviewInline]

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "adaptation":
    #         kwargs["queryset"] = Media.objects.filter(media_type=1)
    #         return Super().formfield_for_manytomany(db_field, request, **kwargs)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


# class UserMangaAdmin(admin.ModelAdmin):
#     list_display = ("user", "manga", "last_read")
#     list_filter = ("user", "last_read")
#     search_fields = ("manga",)
#     inlines = [UserChapterInline]
#     exclude = ("chapters",)


admin.site.register(Session)
admin.site.register(User)
admin.site.register(Referral)
admin.site.register(Campaign)
admin.site.register(MyCustomTag, TagAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(ElitemangaReview)
admin.site.register(Media, MediaAdmin)
admin.site.register(Source)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Review)
admin.site.register(ReviewVote)
admin.site.register(Comment)
# admin.site.register(UserManga, UserMangaAdmin)
