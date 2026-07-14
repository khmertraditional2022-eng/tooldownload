import requests
import re
import urllib.parse

html = requests.get('https://www.shorttv.live/episode/dubbed-reborn-as-the-villain-i-refuse-to-be-framed-27462-1').text

# Nuxt sometimes embeds JSON state in `<script>window.__NUXT__=(...)</script>`
# Let's extract URLs from the HTML directly
links = re.findall(r'href="(/episode/[^"]+)"', html)
episodes = set()
for l in links:
    if '27462' in l:
        episodes.add("https://www.shorttv.live" + l)

print('Found', len(episodes), 'episodes in HTML via href')
if len(episodes) < 10:
    # Try searching the text for Episode numbers or IDs
    match = re.search(r'"episodes":\s*(\[.*?\])\s*,\s*"', html)
    if match:
        print("Found episodes JSON!")
    else:
        # Let's just find any sequence that looks like episode data
        eps = re.findall(r'"seriesId":(\d+),"episodeId":(\d+),"episodeNumber":(\d+)', html)
        print("Found in JSON state:", len(eps))
        print("Sample:", eps[:5])
