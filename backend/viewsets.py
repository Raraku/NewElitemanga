from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import generics
from django.db.models import Q, F
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
    FileUploadParser,
)
from django.utils.decorators import method_decorator
import random
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.vary import vary_on_cookie
from rest_framework.decorators import (
    action,
    api_view,
    renderer_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    SAFE_METHODS,
)
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import status
from .models import (
    Media,
    Review,
    Comment,
    ReviewVote,
    List,
    Announcement,
    Referral,
    Campaign,
)
from users.models import Profile
from .serializers import (
    MediainfoSerializer,
    # ChapterSerializer,
    AnnouncementSerializer,
    AnnouncementMassSerializer,
    ReviewAloneAuthSerializer,
    ReviewAuthenticatedSerializer,
    ReferralSerializer,
    MediaSerializer,
    # ChapterpageSerializer,
    # UserMangaSerializer,
    # UserMangaPingSerializer,
    MediaSearchSerializer,
    ProfileSerializer,
    ProfileImageSerializer,
    ReviewSerializer,
    ListInfoSerializer,
    ListSerializer,
    ReviewAloneSerializer,
    CommentSerializer,
    TagSerializer,
)
from django.contrib.sessions.models import Session
from django_filters import rest_framework as filters
import json
from taggit.models import Tag


class IsAuthorOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user


class IsUserOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10


# Mixed viewsets
class MixedViewSetOperations(ReadOnlyModelViewSet):
    queryset = Media.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = MediainfoSerializer

    @action(detail=False, methods=["get"])
    def get_random_10(self, request):
        no_queryset = list(Media.objects.exclude(status=2))
        queryset = random.sample(no_queryset, 10)
        manga = MediainfoSerializer(queryset, many=True, context={"request": request})
        return Response(manga.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params["search"]
        queryset = Media.objects.filter(
            Q(title__search=query)
            | Q(title__icontains=query)
            | Q(other_names__search=query)
        )
        search_results = MediaSearchSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(search_results.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    @never_cache
    def get_reviews(self, request, pk):
        media = self.get_object()
        queryset = media.review_set.order_by("-created")
        page = self.paginate_queryset(queryset)
        if page is not None:
            if request.user.is_authenticated:
                serializer = ReviewAuthenticatedSerializer(
                    page, many=True, context={"request": request}
                )
                return self.get_paginated_response(serializer.data)
            serializer = ReviewSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        serializer = ReviewSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_review(self, request, pk):
        profile = Profile.objects.get(user=request.user)
        media = self.get_object()
        content = request.data["content"]
        print(request.data)

        try:
            if request.data["scores"]:
                review = Review.objects.create(
                    author=profile,
                    media=media,
                    content=content,
                    originality_score=request.data["originality_score"],
                    plot_score=request.data["plot_score"],
                    characters_score=request.data["characters_score"],
                    quality_score=request.data["quality_score"],
                )
                return Response(status=status.HTTP_201_CREATED)
        except Exception as Exc:
            try:
                review = Review.objects.create(
                    author=profile, media=media, content=content
                )
                return Response(status=status.HTTP_201_CREATED)
            except Exception as Exc:
                print
                return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def get_related_manga(self, request, pk):
        media = self.get_object()
        manga_queryset = media.tags.similar_objects()
        mangas = MediainfoSerializer(
            manga_queryset, many=True, context={"request": request}
        )
        return Response(mangas.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def increment_weekly_reads(self, request, pk):
        media = self.get_object()
        media.weekly_reads = F("weekly_reads") + 1
        media.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def get_all_tags(self, request):
        queryset = Tag.objects.all()
        tags = TagSerializer(queryset, many=True, context={"request", request})
        return Response(tags.data, status=status.HTTP_200_OK)


class MixedinfoViewSet(ReadOnlyModelViewSet):
    """
    Viewset for model listings.
    """

    queryset = Media.objects.all()
    serializer_class = MediainfoSerializer
    pagination_class = PageNumberPagination

    @action(detail=False, methods=["get"])
    def get_top_7(self, request):
        queryset = Media.objects.order_by("-hits")[:7]
        manga = MediainfoSerializer(queryset, many=True, context={"request": request})
        return Response(manga.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_heroes(self, request):
        queryset = Media.objects.filter(rank=1)[:21]
        manga = MediainfoSerializer(queryset, many=True, context={"request": request})
        return Response(manga.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def filter_by_tags(self, request):
        query_params = request.query_params.getlist("tags[]")
        print(query_params)
        tags = []
        for query in query_params:
            tags.append(json.loads(query)["name"])
        queryset = Media.objects.all()
        for tag_id in tags:
            print(tag_id)
            queryset = queryset.filter(tags__name__in=[tag_id])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MediainfoSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        return Response(status=status.HTTP_200_OK)


# Manga only viewsets
class MangainfoViewSet(ReadOnlyModelViewSet):
    """+
    Viewset for model listings.
    """

    queryset = Media.objects.filter(media_type=0)
    lookup_field = "alias"
    serializer_class = MediainfoSerializer
    pagination_class = PageNumberPagination

    @action(detail=False, methods=["get"])
    def filter_by_tags(self, request):
        query_params = request.query_params.getlist("tags[]")
        print(query_params)
        tags = []
        for query in query_params:
            tags.append(json.loads(query)["name"])
        queryset = Media.objects.filter(media_type=0)
        for tag_id in tags:
            print(tag_id)
            queryset = queryset.filter(tags__name__in=[tag_id])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MediainfoSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_top_7(self, request):
        queryset = Media.objects.filter(media_type=0).order_by("-hits")[:7]
        manga = MediainfoSerializer(queryset, many=True, context={"request": request})
        return Response(manga.data)

    @action(detail=False, methods=["get"])
    def get_current_manga(self, request):
        no_queryset = list(Media.objects.filter(media_type=0, status=1))
        if len(no_queryset) >= 10:
            queryset = random.sample(no_queryset, 12)
            manga = MediainfoSerializer(
                queryset, many=True, context={"request": request}
            )
            return Response(manga.data, status=status.HTTP_200_OK)
        else:
            manga = MediainfoSerializer(
                no_queryset, many=True, context={"request": request}
            )
            return Response(manga.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_weekly_manga(self, request):
        queryset = Media.objects.filter(media_type=0).order_by("-weekly_reads")[:6]
        manga = MediainfoSerializer(queryset, many=True, context={"request": request})
        return Response(manga.data, status=status.HTTP_200_OK)


class MangaSearchViewSet(ReadOnlyModelViewSet):
    queryset = Media.objects.filter(media_type=0)
    lookup_field = "alias"
    serializer_class = MediaSearchSerializer


class MangaViewSet(ReadOnlyModelViewSet):
    """
    Viewset for model listings.
    """

    queryset = Media.objects.filter(media_type=0)
    lookup_field = "alias"
    pagination_class = PageNumberPagination
    serializer_class = MediaSerializer

    @action(detail=False, methods=["get"])
    def get_random_10(self, request):
        no_queryset = list(Media.objects.filter(media_type=0))
        queryset = random.sample(no_queryset, 10)
        manga = MediainfoSerializer(queryset, many=True, context={"request": request})
        return Response(manga.data, status=status.HTTP_200_OK)


# Anime only viewsets
class AnimeinfoViewSet(ReadOnlyModelViewSet):
    """
    Viewset for model listings.
    """

    queryset = Media.objects.filter(media_type=1)
    lookup_field = "alias"
    serializer_class = MediainfoSerializer
    pagination_class = PageNumberPagination

    # @action(detail=True, methods=["get"])
    # def add_to_manga(self, request, alias=None):
    #     manga = self.get_object()
    #     if request.user.is_authenticated:
    #         UserManga.objects.get_or_create(
    #             user=request.user, manga=manga, alias=manga.alias
    #         )
    #         return Response(status=status.HTTP_200_OK)
    #     else:
    #         UserManga.objects.get_or_create(
    #             anonymous=Session.objects.get(session_key=request.session.session_key),
    #             manga=manga,
    #         )
    #         return Response(status=status.HTTP_200_OK)
    @action(detail=False, methods=["get"])
    def get_top_7(self, request):
        queryset = Media.objects.filter(media_type=1).order_by("-hits")[:7]
        manga = MediainfoSerializer(queryset, many=True, context={"request": request})
        return Response(manga.data)

    @action(detail=False, methods=["get"])
    def get_current_anime(self, request):
        no_queryset = list(Media.objects.filter(media_type=1, status=1))
        if len(no_queryset) >= 10:
            queryset = random.sample(no_queryset, 12)
            manga = MediainfoSerializer(
                queryset, many=True, context={"request": request}
            )
            return Response(manga.data, status=status.HTTP_200_OK)
        else:
            manga = MediainfoSerializer(
                no_queryset, many=True, context={"request": request}
            )
            return Response(manga.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_unreleased_anime(self, request):
        queryset = Media.objects.filter(media_type=1, status=2)[:5]
        manga = MediainfoSerializer(queryset, many=True, context={"request": request})
        return Response(manga.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_weekly_manga(self, request):
        queryset = (
            Media.objects.filter(media_type=1)
            .exclude(status=2)
            .order_by("-weekly_reads")[:6]
        )
        manga = MediainfoSerializer(queryset, many=True, context={"request": request})
        return Response(manga.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def filter_by_tags(self, request):
        query_params = request.query_params.getlist("tags[]")
        print(query_params)
        tags = []
        for query in query_params:
            tags.append(json.loads(query)["name"])
        queryset = Media.objects.filter(media_type=1)
        for tag_id in tags:
            print(tag_id)
            queryset = queryset.filter(tags__name__in=[tag_id])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MediainfoSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        return Response(status=status.HTTP_200_OK)


class AnimeSearchViewSet(ReadOnlyModelViewSet):
    queryset = Media.objects.filter(media_type=1)
    lookup_field = "alias"
    serializer_class = MediaSearchSerializer


class AnimeViewSet(ReadOnlyModelViewSet):
    """
    Viewset for model listings.
    """

    queryset = Media.objects.filter(media_type=1)
    lookup_field = "alias"
    pagination_class = PageNumberPagination
    serializer_class = MediaSerializer

    @action(detail=False, methods=["get"])
    def get_random_10(self, request):
        no_queryset = list(Media.objects.filter(media_type=1).exclude(status=2))
        queryset = random.sample(no_queryset, 10)
        manga = MediainfoSerializer(queryset, many=True, context={"request": request})
        return Response(manga.data, status=status.HTTP_200_OK)


class ListViewset(ReadOnlyModelViewSet):
    queryset = List.objects.all()
    lookup_field = "slug"
    serializer_class = ListSerializer
    pagination_class = LargeResultsSetPagination

    @action(detail=False, methods=["get"])
    def get_recent_lists(self, request):
        queryset = List.objects.order_by("-date_uploaded")[:7]
        list_data = ListInfoSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(list_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params["search"]
        queryset = List.objects.filter(
            Q(title__search=query) | Q(title__icontains=query)
        )
        search_results = ListInfoSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(search_results.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def get_related_lists(self, request, slug):
        media = self.get_object()
        manga_queryset = media.tags.similar_objects()
        Lists = ListInfoSerializer(
            manga_queryset, many=True, context={"request": request}
        )
        return Response(Lists.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def increment_weekly_reads(self, request, slug):
        Lists = self.get_object()
        Lists.upvotes = F("upvotes") + 1
        Lists.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def get_top_5(self, request):
        queryset = List.objects.order_by("-upvotes")[:5]
        Lists = ListInfoSerializer(queryset, many=True, context={"request": request})
        return Response(Lists.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_recent_5(self, request):
        queryset = List.objects.order_by("-date_uploaded")[:5]
        Lists = ListInfoSerializer(queryset, many=True, context={"request": request})
        return Response(Lists.data, status=status.HTTP_200_OK)


# Add review and comment functionality to lists after release


class AnnouncementViewset(ReadOnlyModelViewSet):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.order_by("-date_written")
    lookup_field = "slug"

    @action(detail=False, methods=["get"])
    def get_recent_announcements(self, request):
        recent = Announcement.objects.order_by("-date_written")[:5]
        serializer = AnnouncementMassSerializer(
            recent, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_new_number(self, request):
        recent = request.query_params.get("last_login")
        queryset = Announcement.objects.filter()
        serializer = AnnouncementMassSerializer(
            queryset, many=True, context={"request", request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(never_cache, name="dispatch")
class AddReview(ModelViewSet):
    serializer_class = ReviewAloneSerializer
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def get_my_reviews(self, request):
        profile = Profile.objects.get(user=request.user)
        queryset = Review.objects.filter(author=profile).order_by("-created")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReviewAloneAuthSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        Reviews = ReviewAloneAuthSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(Reviews.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk):
        profile = Profile.objects.get(user=request.user)
        review = Review.objects.get(pk=pk)
        content = request.data["content"]
        try:
            review = Comment.objects.create(
                author=profile, review=review, content=content
            )
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ReferralViewSet(ReadOnlyModelViewSet):
    serializer_class = ReferralSerializer
    queryset = Referral.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class AddComment(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@method_decorator(never_cache, name="dispatch")
class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsUserOrReadOnly]
    parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        user = self.request.user

        obj = generics.get_object_or_404(queryset, user=user)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class ProfileImageView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileImageSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsUserOrReadOnly]
    parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)

    parser_class = (FileUploadParser,)

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        # file_serializer = ProfileImageSerializer(data=request.data, partial=True)
        # if file_serializer.is_valid():
        #     file_serializer.save()
        return Response(status=status.HTTP_201_CREATED)
        # else:
        #     return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        user = self.request.user

        obj = generics.get_object_or_404(queryset, user=user)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


# External Api Views
@never_cache
@api_view(["GET"])
def get_review_comments(request, pk):
    review = Review.objects.get(pk=pk)
    queryset = Comment.objects.filter(review=review)
    serializer = CommentSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@never_cache
@api_view(["GET"])
def create_increase_referral(request, username_no):
    campaign = Campaign.objects.get(is_active=True)
    owner = Profile.objects.get(slug=username_no)
    referred = Profile.objects.get(user=request.user)
    if owner == referred:
        return Response(
            status=status.HTTP_403_FORBIDDEN,
            data={"error": "You can't invite yourself"},
        )
    if referred.is_referred == True:
        return Response(
            status=status.HTTP_403_FORBIDDEN,
            data={"error": "You have already acknowledged an invitation"},
        )

    referral = Referral.objects.get_or_create(campaign=campaign, owner=owner)[
        0
    ].referrals.add(referred)
    referred.is_referred = True
    referred.save()
    return Response(status=status.HTTP_200_OK, data={"user": owner.username})


@api_view(["GET"])
@never_cache
@permission_classes([IsAuthenticated])
def vote(request, pk):
    review = Review.objects.get(pk=pk)
    choice = request.query_params.get("choice")
    if choice == "like":
        vote = ReviewVote.objects.get_or_create(
            choice="1", user=request.user, user_review=review
        )
        print(vote[1])
        if vote[1] == False:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_201_CREATED)
    if choice == "dislike":
        vote = ReviewVote.objects.get_or_create(
            choice="2", user=request.user, user_review=review
        )
        if vote[1] == False:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@never_cache
@permission_classes([IsAuthenticated])
def devote(request, pk):
    review = Review.objects.get(pk=pk)
    choice = request.query_params.get("choice")
    if choice == "like":
        try:
            vote = ReviewVote.objects.get(
                choice="1", user=request.user, user_review=review
            )
            vote.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as exc:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if choice == "dislike":
        try:
            vote = ReviewVote.objects.get(
                choice="2", user=request.user, user_review=review
            )
            vote.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as exc:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# @never_cache
# @permission_classes([IsAuthenticated])
# def checkVote(request, pk):
#     review = Review.objects.get(pk=pk)
#     queryset = ReviewVote.objects.filter(user=request.user, user_review=review)
#     count = len(queryset)
#     print(count)
#     if count == 0:
#         return Response(
#             data={"like": False, "dislike": False}, status=status.HTTP_200_OK,
#         )
#     if count == 2:
#         return Response(data={"like": True, "dislike": True}, status=status.HTTP_200_OK)
#     if count == 1:
#         number = queryset[0].choice
#         if number == "1":
#             return Response(
#                 data={"like": True, "dislike": False}, status=status.HTTP_200_OK
#             )
#         if number == "2":
#             return Response(
#                 data={"like": False, "dislike": True}, status=status.HTTP_200_OK
#             )
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def addManganeloManga(request):
    print(request.data["title"])
    manga = request.data
    if manga["media_type"] == 1:
        addedManga = Media.objects.get_or_create(
            author=manga["author"],
            title=manga["title"],
            description=manga["description"],
            hits=manga["hits"],
            other_names=manga["other_names"],
            alias=manga["alias"],
            status=manga["status"],
            pre_image_url=manga["image_url"],
            media_type=manga["media_type"],
        )
    if manga["media_type"] == 0:
        addedManga = Media.objects.get_or_create(
            author=manga["author"],
            title=manga["title"],
            description=manga["description"],
            hits=manga["hits"],
            other_names=manga["other_names"],
            alias=manga["alias"],
            status=manga["status"],
            pre_image_url=manga["image_url"],
            media_type=manga["media_type"],
        )
    for tag in manga["tags"]:
        addedManga[0].tags.add(tag)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["get"])
def WeeklyMediaReset(request):
    Media.objects.all().update(weekly_reads=0)
    return Response(status=status.HTTP_201_CREATED)


"""Below this is removed code"""

# @api_view(["post"])
# def addManganeloChapter(request):
#     print(request.data[0])
#     try:
#         for chapter in request.data:
#             Chapter.objects.get_or_create(
#                 manga_alias=chapter["manga_alias"],
#                 title=chapter["title"],
#                 number=chapter["number"],
#                 date_uploaded=chapter["date_uploaded"],
#                 pages=chapter["pages"],
#                 chapter_type=chapter["chapter_type"],
#                 manga=Manga.objects.get(
#                     alias=chapter["manga_alias"], manga_type=chapter["chapter_type"]
#                 ),
#             )
#         return Response(status=status.HTTP_201_CREATED)
#     # serializer = ChapterAddSerializer(data=request.data, many=True)
#     # if serializer.is_valid():
#     #     serializer.save()
#     #     return Response(serializer.data, status.HTTP_201_CREATED)
#     # return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
#     except Exception as exc:
#         return Response(status=status.HTTP_404_NOT_FOUND, data={"error": Exception})

# @action(detail=True, methods=["get"])
# def get_chapters(self, request, alias=None):
#     queryset = Manga.objects.get(alias=alias).chapters.order_by("-number")
#     chapters = ChapterSerializer(queryset, many=True)
#     return Response(chapters.data)

# @action(detail=True, methods=["get"])
# def get_recent_chapters(self, request, alias=None):
#     queryset = Manga.objects.get(alias=alias).chapters.order_by("-date_uploaded")[
#         :3
#     ]
#     chapters = ChapterSerializer(queryset, many=True)
#     return Response(chapters.data)

# @action(detail=True, methods=["get"])
# def get_chapter(self, request, alias=None):
#     number = self.request.query_params.get("number")
#     queryset = Manga.objects.get(alias=alias).chapters.filter(number=number)
#     chapter = ChapterpageSerializer(queryset, many=True)
#     return Response(chapter.data)

# @action(detail=True, methods=["get"])
# def add_to_manga(self, request, alias=None):
#     manga = self.get_object()
#     if request.user.is_authenticated:
#         UserManga.objects.get_or_create(
#             user=request.user, manga=manga, alias=manga.alias
#         )
#         return Response(status=status.HTTP_200_OK)
#     else:
#         UserManga.objects.get_or_create(
#             anonymous=Session.objects.get(session_key=request.session.session_key),
#             manga=manga,
#         )
#         return Response(status=status.HTTP_200_OK)


# class ChapterViewSet(ReadOnlyModelViewSet):
#     serializer_class = ChapterSerializer
#     pagination_class = PageNumberPagination

#     def get_queryset(self):
#         manga = self.request.query_params.get("manga")
#         queryset = Chapter.objects.filter(manga_alias=manga).order_by("-number")
#         return queryset


# class UserMangaViewSet(ReadOnlyModelViewSet):
#     serializer_class = UserMangaSerializer
#     pagination_class = PageNumberPagination
#     lookup_field = "alias"

#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#             queryset = UserManga.objects.filter(user=self.request.user)
#         else:
#             if not self.request.session.session_key:
#                 self.request.session.save()
#             queryset = UserManga.objects.filter(
#                 anonymous=Session.objects.get(
#                     session_key=self.request.session.session_key
#                 )
#             )
#         return queryset

#     @action(detail=True, methods=["get"])
#     def add_chapter(self, request, manga=None):
#         usermanga = self.get_object()
#         chapid = request.query_params.get("chapter_id")
#         usermanga.chapters.add(Chapter.objects.get(chapter_id=chapid))
#         return Response(status=status.HTTP_200_OK)

#     @action(detail=False, methods=["get"])
#     def get_favorites(self, request):
#         if self.request.user.is_authenticated:
#             queryset = UserManga.objects.filter(user=request.user, isfavorite=True)
#         else:
#             if not self.request.session.session_key:
#                 self.request.session.save()
#             queryset = UserManga.objects.filter(
#                 anonymous=Session.objects.get(
#                     session_key=self.request.session.session_key
#                 ),
#                 isfavorite=True,
#             )
#         Usermanga = UserMangaSerializer(queryset, many=True)
#         return Response(Usermanga.data, status=status.HTTP_200_OK)

#     @action(detail=True, methods=["get"])
#     def add_to_favorites(self, request, alias=None):
#         manga = self.get_object
#         choice = request.query_params.get("choice")
#         if choice == True:
#             manga.isfavorite = True
#         else:
#             manga.isfavorite = False
#         manga.save()


# class UserMangaPingViewset(ModelViewSet):
#     serializer_class = UserMangaPingSerializer
#     lookup_field = "alias"

#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#             queryset = UserManga.objects.filter(user=self.request.user)
#         else:
#             if not self.request.session.session_key:
#                 self.request.session.save()
#             queryset = UserManga.objects.filter(
#                 anonymous=Session.objects.get(
#                     session_key=self.request.session.session_key
#                 )
#             )
#         return queryset


# class UserMangaStateViewset(ModelViewSet):
#     serializer_class = UserMangaPingSerializer
#     lookup_field = "alias"

#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#             queryset = UserManga.objects.filter(user=self.request.user)
#         else:
#             if not self.request.session.session_key:
#                 self.request.session.save()
#             queryset = UserManga.objects.filter(
#                 anonymous=Session.objects.get(
#                     session_key=self.request.session.session_key
#                 )
#             )
#         return queryset
