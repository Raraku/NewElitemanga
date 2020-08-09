import lxml
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import concurrent.futures
import threading
import time
import json

# Create your views here.
months = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}
thread_local = threading.local()


def scraper(manga_link):
    def get_session():
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
        return thread_local.session

    manga = requests.get(manga_link)
    manga = BeautifulSoup(manga.content, "lxml")
    print("scrape started")
    title = manga.find(itemprop="name").get_text()
    alias = title.lower().replace(" ", "-")

    def myconverter(o):
        if isinstance(o, datetime):
            return o.__str__()

    def scrapeManga(manga):
        # get image
        title = manga.find(itemprop="name").get_text()
        alias = title.lower().replace(" ", "-")
        manga_image = manga.find(itemprop="image")
        manga_image = manga_image["data-src"]
        # title and alternative names
        print(title)
        info = manga.find_all(
            string=["Type:", "Status:", "Aired:", "Premiered:", "Studios:", "Genres:"]
        )
        g = manga.find_all(class_="spaceit_pad")[:3]
        other_names = ""
        for t in g:
            other_names = other_names + t.text
        other_names.replace("  ", " ")
        author = info[5].parent.next_sibling.next_sibling.text
        status = info[2].parent.next_sibling.strip()
        if status == "Currently Airing":
            status = 1
        if status == "finished":
            status = 0
        if status == "Not yet aired":
            status = 2
        if len(info) == 7:
            tags_string = info[6].parent.parent.find_all("a")
        else:
            tags_string = info[5].parent.parent.find_all("a")
        tags = []
        for tag in tags_string:
            tags.append(tag["title"])
        # time and last_updated

        hits = int(
            manga.find(string="Members:").parent.next_sibling.strip().replace(",", "")
        )
        description = manga.find(itemprop="description")
        description = description.text.replace("[Written by MAL Rewrite]", "").strip()
        print("here")
        manga_value = {
            "title": title,
            "image_url": manga_image,
            "other_names": other_names,
            "author": author,
            "tags": tags,
            "status": status,
            "hits": hits,
            "alias": alias,
            "description": description,
            "media_type": 1,
        }

        print(manga_value)
        return manga_value

    print("here")
    start_time = time.time()
    manga = scrapeManga(manga)
    print("aha")
    duration = time.time() - start_time
    print(f"Downloaded all in {duration} seconds")
    # Step 1
    # post manga
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        "http://127.0.0.1:8000/add-manganelo-manga/", json=manga, headers=headers,
    )
    # print(response.text)
    print(response.text)
    return title + " done"
    # post tags for manga
