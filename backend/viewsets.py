from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import action, api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import status
from .models import Manga, Chapter, UserManga, MangaTag
from .serializers import (
    MangainfoSerializer,
    ChapterSerializer,
    MangaSerializer,
    ChapterpageSerializer,
    UserMangaSerializer,
    UserMangaPingSerializer,
    MangaSearchSerializer,
)
from django.contrib.sessions.models import Session
from django_filters import rest_framework as filters
import json


class MangainfoViewSet(ReadOnlyModelViewSet):
    """
    Viewset for model listings.
    """

    queryset = Manga.objects.order_by("-hits")
    lookup_field = "alias"
    serializer_class = MangainfoSerializer
    pagination_class = PageNumberPagination

    @action(detail=True, methods=["get"])
    def add_to_manga(self, request, alias=None):
        manga = self.get_object()
        if request.user.is_authenticated:
            UserManga.objects.get_or_create(
                user=request.user, manga=manga, alias=manga.alias
            )
            return Response(status=status.HTTP_200_OK)
        else:
            UserManga.objects.get_or_create(
                anonymous=Session.objects.get(session_key=request.session.session_key),
                manga=manga,
            )
            return Response(status=status.HTTP_200_OK)


class MangaSearchViewSet(ReadOnlyModelViewSet):
    queryset = Manga.objects.all()
    lookup_field = "alias"
    serializer_class = MangaSearchSerializer


class MangaViewSet(ReadOnlyModelViewSet):
    """
    Viewset for model listings.
    """

    queryset = Manga.objects.all()
    lookup_field = "alias"
    pagination_class = PageNumberPagination
    serializer_class = MangaSerializer

    @action(detail=True, methods=["get"])
    def get_chapters(self, request, alias=None):
        queryset = Manga.objects.get(alias=alias).chapters.order_by("-number")
        chapters = ChapterSerializer(queryset, many=True)
        return Response(chapters.data)

    @action(detail=True, methods=["get"])
    def get_recent_chapters(self, request, alias=None):
        queryset = Manga.objects.get(alias=alias).chapters.order_by("-date_uploaded")[
            :3
        ]
        chapters = ChapterSerializer(queryset, many=True)
        return Response(chapters.data)

    @action(detail=True, methods=["get"])
    def get_chapter(self, request, alias=None):
        number = self.request.query_params.get("number")
        queryset = Manga.objects.get(alias=alias).chapters.filter(number=number)
        chapter = ChapterpageSerializer(queryset, many=True)
        return Response(chapter.data)

    @action(detail=True, methods=["get"])
    def add_to_manga(self, request, alias=None):
        manga = self.get_object()
        if request.user.is_authenticated:
            UserManga.objects.get_or_create(
                user=request.user, manga=manga, alias=manga.alias
            )
            return Response(status=status.HTTP_200_OK)
        else:
            UserManga.objects.get_or_create(
                anonymous=Session.objects.get(session_key=request.session.session_key),
                manga=manga,
            )
            return Response(status=status.HTTP_200_OK)


class ChapterViewSet(ReadOnlyModelViewSet):
    serializer_class = ChapterSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        manga = self.request.query_params.get("manga")
        queryset = Chapter.objects.filter(manga_alias=manga).order_by("-number")
        return queryset


class UserMangaViewSet(ReadOnlyModelViewSet):
    serializer_class = UserMangaSerializer
    pagination_class = PageNumberPagination
    lookup_field = "alias"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = UserManga.objects.filter(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.save()
            queryset = UserManga.objects.filter(
                anonymous=Session.objects.get(
                    session_key=self.request.session.session_key
                )
            )
        return queryset

    @action(detail=True, methods=["get"])
    def add_chapter(self, request, manga=None):
        usermanga = self.get_object()
        chapid = request.query_params.get("chapter_id")
        usermanga.chapters.add(Chapter.objects.get(chapter_id=chapid))
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_favorites(self, request):
        if self.request.user.is_authenticated:
            queryset = UserManga.objects.filter(user=request.user, isfavorite=True)
        else:
            if not self.request.session.session_key:
                self.request.session.save()
            queryset = UserManga.objects.filter(
                anonymous=Session.objects.get(
                    session_key=self.request.session.session_key
                ),
                isfavorite=True,
            )
        Usermanga = UserMangaSerializer(queryset, many=True)
        return Response(Usermanga.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def add_to_favorites(self, request, alias=None):
        manga = self.get_object
        choice = request.query_params.get("choice")
        if choice == True:
            manga.isfavorite = True
        else:
            manga.isfavorite = False
        manga.save()


class UserMangaPingViewset(ModelViewSet):
    serializer_class = UserMangaPingSerializer
    lookup_field = "alias"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = UserManga.objects.filter(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.save()
            queryset = UserManga.objects.filter(
                anonymous=Session.objects.get(
                    session_key=self.request.session.session_key
                )
            )
        return queryset


class UserMangaStateViewset(ModelViewSet):
    serializer_class = UserMangaPingSerializer
    lookup_field = "alias"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = UserManga.objects.filter(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.save()
            queryset = UserManga.objects.filter(
                anonymous=Session.objects.get(
                    session_key=self.request.session.session_key
                )
            )
        return queryset


@api_view(["POST"])
def addManganeloManga(request):
    print(request.data["title"])
    manga = request.data
    addedManga = Manga.objects.get_or_create(
        manga_type=manga["manga_type"],
        chapters_length=manga["chapters_length"],
        author=manga["author"],
        last_updated=manga["last_updated"],
        title=manga["title"],
        description=manga["description"],
        hits=manga["hits"],
        other_names=manga["other_names"],
        alias=manga["alias"],
        status=manga["status"],
        image_url=manga["image_url"],
    )
    for tag in manga["tags"]:
        MangaTag.objects.get_or_create(name=tag)[0].manga_set.add(addedManga[0])
    return Response(status=status.HTTP_201_CREATED)


@api_view(["post"])
def addManganeloChapter(request):
    print(request.data[0])
    try:
        for chapter in request.data:
            Chapter.objects.get_or_create(
                manga_alias=chapter["manga_alias"],
                title=chapter["title"],
                number=chapter["number"],
                date_uploaded=chapter["date_uploaded"],
                pages=chapter["pages"],
                chapter_type=chapter["chapter_type"],
                manga=Manga.objects.get(
                    alias=chapter["manga_alias"], manga_type=chapter["chapter_type"]
                ),
            )
        return Response(status=status.HTTP_201_CREATED)
    # serializer = ChapterAddSerializer(data=request.data, many=True)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status.HTTP_201_CREATED)
    # return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    except Exception as exc:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": Exception})
