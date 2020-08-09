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
    title = manga.find("h1").get_text()
    alias = title.lower().replace(" ", "-")

    def myconverter(o):
        if isinstance(o, datetime):
            return o.__str__()

    def scrapeManga(manga):
        # get image

        manga_image = manga.find(class_="info-image").img
        manga_image = manga_image["src"]
        # title and alternative names
        title = manga.find("h1").get_text()
        print(title)
        info = manga.find_all(class_="table-value")
        other_names = info[0].get_text()
        author = info[1].get_text()
        status = info[2].get_text().lower()
        if status == "ongoing":
            status = 1
        if status == "finished":
            status = 0
        tags = info[3].get_text().strip("\n")
        tags = tags.split("-")
        for tag in tags:
            no = tags.index(tag)
            tag = tag.strip()
            tags[no] = tag
        # time and last_updated
        info2 = manga.find_all("span", class_="stre-value")
        last_updated = info2[0].get_text()
        month_value = months[last_updated[:3]]
        last_updated = last_updated[3:]
        last_updated = str(month_value) + last_updated
        last_updated = str(datetime.strptime(last_updated, "%m %d,%Y - %H:%M %p"))
        hits = int(info2[1].get_text().replace(",", ""))
        description = manga.find("div", class_="panel-story-info-description")
        try:
            description = description.contents[5].get_text() + description.contents[
                6
            ].strip("\n")
        except Exception as exc:
            description = " we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!! we are otakus!!"
        alias = title.lower().replace(" ", "-")
        # get chapters and pages
        chapters = manga.find_all(class_="chapter-name")
        chapters.reverse()
        chapters_len = len(chapters)
        manga_value = {
            "title": title,
            "image_url": manga_image,
            "other_names": other_names,
            "chapters_length": chapters_len,
            "author": author,
            "tags": tags,
            "status": status,
            "last_updated": last_updated,
            "hits": hits,
            "alias": alias,
            "description": description,
            "media_type": 0,
        }
        return manga_value

    start_time = time.time()
    manga = scrapeManga(manga)
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
