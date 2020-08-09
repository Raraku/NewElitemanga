from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from backend.models import Media
from bs4 import BeautifulSoup
import requests
import lxml
from .scraper import scraper
import json


@api_view(["get"])
def updateUpcomingAnime(request):
    # Updating old results to check release date later
    donemanga = []
    tobedonemanga = []
    savedmanga = []
    updated_manga = requests.get("https://myanimelist.net/")
    mangasoup = BeautifulSoup(updated_manga.content, "lxml")
    mangasoup = mangasoup.find_all("div", class_="ranking-digest")
    mangasoup = mangasoup[1]
    mangasoup = mangasoup.ul
    mangasoup = mangasoup.find_all("li")
    for anime in mangasoup:
        tobedonemanga.append(anime.a["href"])
    with open("backend/mal/upcominganime.json", "r") as target:
        donemanga = json.load(target)
    for link in tobedonemanga:
        if link in donemanga:
            pass
        else:
            scraper(link)
            savedmanga.append(link)

    with open("backend/mal/upcominganime.json", "w") as target:
        donemanga = savedmanga + donemanga
        json.dump(donemanga, target)
    return Response(status=status.HTTP_200_OK)

@api_view(["get"])
def updateMangaImage(request):
    manga=Media.objects.filter(media_type=0)
    for item in manga:
        item.pre_image_url = item.imageurl