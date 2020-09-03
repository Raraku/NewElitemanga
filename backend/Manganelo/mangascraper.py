import json
import scraper
import concurrent.futures
import threading
from mangalinks import current_links

donemanga = []
tobedonemanga = []

with open("donemanga.json", "r") as target:
    donemanga = json.load(target)


for link in current_links:
    if link in donemanga:
        pass
    else:
        tobedonemanga.append(link)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(scraper.scraper, tobedonemanga)
for element in tobedonemanga:
    donemanga.append(element)
with open("donemanga.json", "w") as target:
    json.dump(donemanga, target)
