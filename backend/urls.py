from rest_framework.routers import DefaultRouter
from .viewsets import (
    MangainfoViewSet,
    MangaViewSet,
    UserMangaViewSet,
    UserMangaPingViewset,
    UserMangaStateViewset,
    ChapterViewSet,
    MangaSearchViewSet,
    addManganeloChapter,
    addManganeloManga,
)
from django.urls import path


router = DefaultRouter()
router.register(r"mangainfo", MangainfoViewSet, "mangainfo")
router.register(r"manga", MangaViewSet)
router.register(r"chapterlist", ChapterViewSet, base_name="chapterlist")
router.register(r"usermanga", UserMangaViewSet, base_name="usermanga")
router.register(r"ping", UserMangaPingViewset, base_name="ping")
router.register(r"usermangastate", UserMangaStateViewset, base_name="usermangastate")
router.register(r"mangasearch", MangaSearchViewSet)
urlpatterns = [
    path("add-manganelo-manga/", addManganeloManga),
    path("add-manganelo-chapter/", addManganeloChapter),
]

urlpatterns += router.urls
