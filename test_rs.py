import re
import json
import urllib.request

url = "https://www.reelshort.com/episodes/episode-1-now-i-m-your-ceo-ex-husband-6a3ba36a54aeacec4308eee8-r92hxhq31m"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
    if match:
        data = json.loads(match.group(1))
        # Save to file to inspect
        with open('next_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print("Data saved to next_data.json")
except Exception as e:
    print(f"Error: {e}")
