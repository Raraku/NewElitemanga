# serialize models
from rest_framework import serializers
from .models import Manga, MangaTag, UserManga, Chapter
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
import json


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MangaTag
        fields = [
            "name",
        ]


class MangainfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manga
        fields = [
            "alias",
            "author",
            "title",
            "image_url",
            "description",
            "rank",
            "hits",
            "last_updated",
        ]
        read_only_fields = [
            "author",
            "title",
            "image_url",
            "rank",
            "hits",
            "last_updated",
        ]


class MangaSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = [
            "alias",
            "author",
            "title",
            "image_url",
            "description",
            "tags",
            "rank",
            "other_names",
            "hits",
            "last_updated",
        ]
        read_only_fields = [
            "author",
            "title",
            "image_url",
            "other_names" "rank",
            "hits",
            "last_updated",
        ]


class MangaSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Manga
        fields = [
            "author",
            "alias",
            "chapters_length",
            "title",
            "image_url",
            "description",
            "tags",
            "image_url",
            "other_names",
            "status",
            "hits",
            "last_updated",
        ]


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["number", "date_uploaded", "title"]


class ChapterpageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["number", "title", "pages", "date_uploaded"]


class UserMangaSerializer(serializers.ModelSerializer):
    manga = MangainfoSerializer()

    class Meta:
        model = UserManga
        fields = ["manga", "last_read", "isfavorite", "id"]
        depth = 1


class UserMangaPingSerializer(serializers.ModelSerializer):
    last_read = serializers.DateTimeField()

    class Meta:
        model = UserManga
        fields = ["alias", "last_read"]

