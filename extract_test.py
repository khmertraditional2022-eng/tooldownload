import urllib.request
import re
url = "https://www.reelshort.com/movie/real-or-fake-i-decide-6a13c64994826c1ddf0822ab"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    episodes = set(re.findall(r'/episodes/[^\"]+', html))
    print(f"Found {len(episodes)} episodes in movie page.")
    if episodes:
        for ep in list(episodes)[:5]:
            print(ep)
except Exception as e:
    print(e)
