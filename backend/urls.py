from rest_framework.routers import DefaultRouter
from .viewsets import (
    MangainfoViewSet,
    MangaViewSet,
    # UserMangaViewSet,
    # UserMangaPingViewset,
    # UserMangaStateViewset,
    MangaSearchViewSet,
    AnimeinfoViewSet,
    AnimeViewSet,
    AnimeSearchViewSet,
    AddReview,
    ProfileView,
    MixedViewSetOperations,
    addManganeloManga,
    vote,
    devote,
    AddComment,
    ListViewset,
    get_review_comments,
    WeeklyMediaReset,
    MixedinfoViewSet,
    ProfileImageView,
    ReferralViewSet,
    AnnouncementViewset,
    create_increase_referral,
)
from .mal.specops import updateUpcomingAnime
from django.urls import path
from .views import verify_email


router = DefaultRouter()
router.register(r"mangainfo", MangainfoViewSet, "mangainfo")
router.register(r"manga", MangaViewSet, "manga")
router.register(r"mixed", MixedViewSetOperations, "mixed")
router.register(r"mixedinfo", MixedinfoViewSet, "mixedinfo")
router.register(r"user-review", AddReview)
router.register(r"mangasearch", MangaSearchViewSet, "mangasearch")
router.register(r"animeinfo", AnimeinfoViewSet, "animeinfo")
router.register(r"anime", AnimeViewSet, "anime")
router.register(r"announcement", AnnouncementViewset, "announcements")
router.register(r"user-review", AddReview)
# router.register(r"invites", ReferralViewSet)
router.register(r"lists", ListViewset)
router.register(r"animesearch", AnimeSearchViewSet, "animesearch")
urlpatterns = [
    path("add-manganelo-manga/", addManganeloManga),
    path("vote-review/<int:pk>/", vote),
    path("devote-review/<int:pk>/", devote),
    path("review-comment/<int:pk>/", get_review_comments),
    path("invites/<str:username_no>/", create_increase_referral),
    path("profile/", ProfileView.as_view()),
    path("profile-upload/", ProfileImageView.as_view()),
    path("reset-manga-weekly/", WeeklyMediaReset),
    path("verify-email/", verify_email),
    path("update_upcoming/", updateUpcomingAnime)
    # path("add-manganelo-chapter/", addManganeloChapter),
]

urlpatterns += router.urls
