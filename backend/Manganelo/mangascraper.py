import json
import scraper
import concurrent.futures
import threading

donemanga = []
tobedonemanga = []

with open("donemanga.json", "r") as target:
    donemanga = json.load(target)

current_links = [
    "https://manganelo.com/manga/read_boku_no_hero_academia_manga",
    "https://manganelo.com/manga/boruto_naruto_next_generations",
    "https://manganelo.com/manga/kimetsu_no_yaiba",
    "https://manganelo.com/manga/kxqh9261558062112",
    "https://manganelo.com/manga/read_naruto_manga_online_free3",
    "https://manganelo.com/manga/pn918005",
    "https://manganelo.com/manga/tower_of_god_manga",
    "https://manganelo.com/manga/ilsi12001567132882",
    "https://manganelo.com/manga/read_fullmetal_alchemist_manga",
    "https://manganelo.com/manga/hgvu275071566265053",
    "https://manganelo.com/manga/read_one_punch_man_manga_online_free3",
    "https://manganelo.com/manga/ueb5218786",
    "https://manganelo.com/manga/read_death_note_manga_online",
    "https://manganelo.com/manga/read_one_piece_manga_online_free4",
    "https://manganelo.com/manga/dnha19771568647794",
    "https://manganelo.com/manga/read_fairy_tail_manga_online_for_free",
    "https://manganelo.com/manga/read_the_god_of_high_school_manga",
]
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
