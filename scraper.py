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


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


chapters_list = []
manga = requests.get("https://manganelo.com/manga/read_naruto_manga_online_free3")
manga = BeautifulSoup(manga.content, "lxml")
title = manga.find("h1").get_text()
alias = title.lower().replace(" ", "-")


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def download_chapter(chapter):
    session = get_session()
    chapter_title = chapter.get_text()
    number = chapter["href"].split("_").pop()

    # get chapter time uploaded
    time_uploaded = chapter.next_sibling.next_sibling.next_sibling.next_sibling["title"]
    month_value = months[time_uploaded[:3]]
    time_uploaded = time_uploaded[3:]
    time_uploaded = str(month_value) + time_uploaded
    time_uploaded = str(datetime.strptime(time_uploaded, "%m %d,%Y %H:%M"))
    # get pages
    page = session.get(chapter["href"])
    page = BeautifulSoup(page.content, "lxml")
    page = page.find(class_="container-chapter-reader")
    page = page.find_all("img")
    pages = []
    for image in page:
        pages.append(image["src"])
    value = {
        "manga_alias": alias,
        "title": chapter_title,
        "number": number,
        "date_uploaded": time_uploaded,
        "pages": pages,
        "chapter_type": 0,
    }
    print(value)
    chapters_list.append(value)


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
    with concurrent.futures.ThreadPoolExecutor(max_workers=23) as executor:
        executor.map(download_chapter, chapters)
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
        "manga_type": 0,
    }
    return manga_value


start_time = time.time()
manga = scrapeManga(manga)
duration = time.time() - start_time
print(f"Downloaded all in {duration} seconds")
# Step 1
# post manga
headers = {"Content-Type": "application/json"}

# response = requests.post(
#     "http://localhost:8000/add-manganelo-manga/", json=manga, headers=headers
# )

chapter_response = requests.post(
    "http://localhost:8000/add-manganelo-chapter/", json=chapters_list, headers=headers
)
# print(response.text)
print(chapter_response.text)
# post tags for manga
