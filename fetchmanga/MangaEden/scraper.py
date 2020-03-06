# from backend.models import Manga, Chapter, MangaTag
import json
import concurrent.futures
import threading
import time
import requests

import datetime


thread_local = threading.local()
number = 0


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


chapters_l = []


def getChapter(chapter):
    session = get_session()
    chapter_response = session.get(
        f"https://www.mangaeden.com/api/chapter/{chapter[3]}/"
    )
    chapter_response = chapter_response.json()
    chapter_response = chapter_response["images"]
    raw_date = datetime.datetime.fromtimestamp(chapter[1])
    raw_date = raw_date.replace(minute=0, hour=0, second=0)
    print(chapter_response, chapter)
    chapters_l.append(chapter_response)
    # Chapter.objects.get_or_create(
    #     number=chapter[0],
    #     date_created=raw_date,
    #     title=chapter[2],
    #     chapter_id=chapter[3],
    #     pages=chapter_response,
    #     manga=Manga.objects.get(alias=alias, manga_type=0),
    #     manga_alias=alias,
    # )
    print(str(chapter[0]) + " done.")


def scrapeManga(alias):
    with open("mangaid.json", "r") as target:
        data = json.load(target)
    query = data[alias]
    try:
        fetch = requests.Session()
        response = fetch.get(f"https://www.mangaeden.com/api/manga/{query}/")
        response.raise_for_status()
        response = response.json()
        # manga time uploaded
        raw_date = datetime.datetime.fromtimestamp(response["created"])
        raw_date = raw_date.replace(minute=0, hour=0, second=0)
        time_uploaded = raw_date
        # chapter length
        chapters_length = response["chapters_len"]
        released = response["released"]
        description = response["description"]
        hits = response["hits"]
        image_url = response["imageURL"]
        raw_last_chapter_date = datetime.datetime.fromtimestamp(
            response["last_chapter_date"]
        )
        raw_last_chapter_date = raw_last_chapter_date.replace(
            minute=0, hour=0, second=0
        )
        last_updated = raw_last_chapter_date
        title = response["title"]
        keywords = " ".join(response["title_kw"])
        status = response["status"]
        starts_with = response["startsWith"]
        keywords = starts_with + keywords
        baka = response["baka"]
        author = response["author"]
        artist = response["artist"]
        manga_type = 0
        print(manga_type, chapters_length, author, released, last_updated, title)
        # Manga.objects.get_or_create(
        #     manga_type=manga_type,
        #     chapters_length=chapters_length,
        #     author=author,
        #     released=released,
        #     last_updated=last_updated,
        #     title=title,
        #     description=description,
        #     hits=hits,
        #     other_names=keywords,
        #     alias=alias,
        #     status=status,
        #     image_url=image_url,
        # )
        # for genre in response["categories"]:
        #     Manga.objects.get(alias=alias, manga_type=0).tags.add(
        #         MangaTag.objects.get_or_create(name=genre)[0]
        #     )
        response["chapters"].reverse()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(getChapter, response["chapters"])
        with open("mangachapters/{}.json".format(alias), "w") as target:
            json.dump(response["chapters"], target)
    except requests.exceptions.HTTPError:
        response.raise_for_status()
    return len(response["chapters"])


start_time = time.time()
manga = scrapeManga("boku-no-hero-academia")
duration = time.time() - start_time
print(duration)
print(manga)
print(len(chapters_l))
