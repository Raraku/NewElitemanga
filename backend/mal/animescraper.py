import json
import scraper
import concurrent.futures
import threading
from animelinks import current_links

donemanga = []
tobedonemanga = []

with open("doneanime.json", "r") as target:
    donemanga = json.load(target)


for link in current_links:
    if link in donemanga:
        pass
    else:
        tobedonemanga.append(link)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(scraper.scraper, tobedonemanga)
# for element in tobedonemanga:
#     scraper.scraper(element)
for element in tobedonemanga:
    donemanga.append(element)
with open("doneanime.json", "w") as target:
    json.dump(donemanga, target)
