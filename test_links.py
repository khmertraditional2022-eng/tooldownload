import urllib.request
import re

url = "https://www.reelshort.com/movie/now-i-m-your-ceo-ex-husband-6a3ba36a54aeacec4308eee8"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # Find all episode links in HTML
    links = re.findall(r'href="([^"]+episode-\d+[^"]+)"', html)
    print(f"Found {len(links)} episode links")
    for link in list(set(links))[:10]:
        print(link)
except Exception as e:
    print(f"Error: {e}")
