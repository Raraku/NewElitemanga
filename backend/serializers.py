# serialize models
from rest_framework import serializers
from .models import (
    Media,
    Review,
    Comment,
    ElitemangaReview,
    List,
    ListSection,
    MyCustomTag,
    SourceLink,
    ReviewVote,
    Announcement,
)
from users.models import Profile
import json
from taggit.models import Tag


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self._choices[obj]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "id"]


class ElitemangaReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElitemangaReview
        fields = [
            "originality",
            "originality_score",
            "plot",
            "plot_score",
            "characters",
            "characters_score",
            "quality",
            "quality_score",
            "remark",
            "total_score",
        ]
        read_only_fields = [
            "originality",
            "originality_score",
            "plot",
            "plot_score",
            "characters",
            "characters_score",
            "quality",
            "quality_score",
            "remark",
            "total_score",
        ]


class MediainfoSerializer(serializers.HyperlinkedModelSerializer):
    rank = ChoiceField(choices=Media.RANK)

    class Meta:
        model = Media
        fields = [
            "alias",
            "author",
            "title",
            "id",
            "image_url",
            "description",
            "rank",
            "hits",
            "media_type",
        ]
        read_only_fields = [
            "author",
            "title",
            "id",
            "image_url",
            "rank",
            "hits",
            "media_type",
        ]


class MediaSearchSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    rank = ChoiceField(choices=Media.RANK)

    class Meta:
        model = Media
        fields = [
            "alias",
            "author",
            "title",
            "image_url",
            "description",
            "tags",
            "id",
            "rank",
            "other_names",
            "hits",
            "media_type",
        ]
        read_only_fields = [
            "author",
            "title",
            "image_url",
            "other_names",
            "rank",
            "hits",
        ]


class ThroughSourceSerializer(serializers.ModelSerializer):
    official = serializers.BooleanField(source="source.official")
    name = serializers.CharField(source="source.name")
    homepage = serializers.URLField(source="source.homepage")
    image = serializers.ImageField(source="source.image")
    description = serializers.CharField(source="source.description")

    class Meta:
        model = SourceLink
        fields = ("link", "official", "name", "homepage", "image", "description")


class MediaSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    rank = ChoiceField(choices=Media.RANK)
    elitemangareview = ElitemangaReviewSerializer()
    sources = ThroughSourceSerializer(source="sourcelink_set", many=True)

    class Meta:
        model = Media
        fields = [
            "author",
            "alias",
            "chapters_length",
            "title",
            "id",
            "image_url",
            "description",
            "sources",
            "elitemangareview",
            "tags",
            "image_url",
            "rank",
            "other_names",
            "status",
            "hits",
            "weekly_reads",
            "media_type",
        ]
        read_only_fields = [
            "author",
            "alias",
            "chapters_length",
            "title",
            "id",
            "image_url",
            "elitemangareview",
            "rank",
            "description",
            "tags",
            "media_type",
            "image_url",
            "other_names",
            "status",
            "hits",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["level", "avatar", "username", "date_joined"]
        read_only_fields = [
            "level",
        ]


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar, username"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", "created", "content", "id"]
        read_only_fields = ["author", "content", "id"]
        depth = 1


class ReviewAuthenticatedSerializer(serializers.ModelSerializer):
    comment_number = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True, required=False)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "content",
            "author",
            "created",
            "id",
            "comment_number",
            "comment_set",
            "is_liked",
            "originality_score",
            "plot_score",
            "characters_score",
            "quality_score",
            "likes",
            "dislikes",
        ]
        depth = 1

    def get_is_liked(self, obj):
        queryset = ReviewVote.objects.filter(
            user=self.context["request"].user, user_review=obj
        )
        count = len(queryset)
        print(count)
        if count == 0:
            return {"like": False, "dislike": False}
        if count == 2:
            return {"like": True, "dislike": True}
        if count == 1:
            number = queryset[0].choice
            if number == "1":
                return {"like": True, "dislike": False}
            if number == "2":
                return {"like": False, "dislike": True}

    def get_comment_number(self, obj):
        return obj.comment_set.count()

    def get_likes(self, obj):
        return obj.review_vote.filter(choice="1").count()

    def get_dislikes(self, obj):
        return obj.review_vote.filter(choice="2").count()


class ReviewSerializer(serializers.ModelSerializer):
    comment_number = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True, required=False)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "content",
            "author",
            "created",
            "id",
            "comment_number",
            "comment_set",
            "originality_score",
            "plot_score",
            "characters_score",
            "quality_score",
            "likes",
            "dislikes",
        ]
        depth = 1

    def get_comment_number(self, obj):
        return obj.comment_set.count()

    def get_likes(self, obj):
        return obj.review_vote.filter(choice="1").count()

    def get_dislikes(self, obj):
        return obj.review_vote.filter(choice="2").count()


class ReviewAloneSerializer(serializers.ModelSerializer):
    comment_number = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True, required=False)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    media = MediainfoSerializer()

    class Meta:
        model = Review
        fields = [
            "content",
            "author",
            "created",
            "id",
            "comment_number",
            "comment_set",
            "media",
            "originality_score",
            "plot_score",
            "characters_score",
            "quality_score",
            "likes",
            "dislikes",
        ]
        depth = 1

    def get_comment_number(self, obj):
        return obj.comment_set.count()

    def get_likes(self, obj):
        return obj.review_vote.filter(choice="1").count()

    def get_dislikes(self, obj):
        return obj.review_vote.filter(choice="2").count()


class ReviewAloneAuthSerializer(serializers.ModelSerializer):
    comment_number = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True, required=False)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    media = MediainfoSerializer()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "content",
            "author",
            "created",
            "id",
            "comment_number",
            "comment_set",
            "is_liked",
            "media",
            "originality_score",
            "plot_score",
            "characters_score",
            "quality_score",
            "likes",
            "dislikes",
        ]
        depth = 1

    def get_is_liked(self, obj):
        queryset = ReviewVote.objects.filter(
            user=self.context["request"].user, user_review=obj
        )
        count = len(queryset)
        print(count)
        if count == 0:
            return {"like": False, "dislike": False}
        if count == 2:
            return {"like": True, "dislike": True}
        if count == 1:
            number = queryset[0].choice
            if number == "1":
                return {"like": True, "dislike": False}
            if number == "2":
                return {"like": False, "dislike": True}

    def get_comment_number(self, obj):
        return obj.comment_set.count()

    def get_likes(self, obj):
        return obj.review_vote.filter(choice="1").count()

    def get_dislikes(self, obj):
        return obj.review_vote.filter(choice="2").count()


class ListInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ["title", "image", "slug"]


class ListSectionSerializer(serializers.ModelSerializer):
    media = serializers.StringRelatedField()

    class Meta:
        model = ListSection
        fields = ["media", "review", "position"]


class MyTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCustomTag
        fields = [
            "name",
        ]


class ListSerializer(serializers.ModelSerializer):
    listsection_set = ListSectionSerializer(many=True)
    tags = MyTagSerializer(many=True)

    class Meta:

        model = List
        fields = [
            "title",
            "intro",
            "upvotes",
            "date_uploaded",
            "image",
            "slug",
            "listsection_set",
            "tags",
        ]
        depth = 1


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["title", "content", "date_written", "slug"]


class AnnouncementMassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["title", "date_written", "slug"]


# class ChapterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Chapter
#         fields = ["number", "date_uploaded", "title"]


# class ChapterpageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Chapter
#         fields = ["number", "title", "pages", "date_uploaded"]


# class UserMangaSerializer(serializers.ModelSerializer):
#     manga = MangainfoSerializer()

#     class Meta:
#         model = UserManga
#         fields = ["manga", "last_read", "isfavorite", "id"]
#         depth = 1


# class UserMangaPingSerializer(serializers.ModelSerializer):
#     last_read = serializers.DateTimeField()

#     class Meta:
#         model = UserManga
#         fields = ["alias", "last_read"]
