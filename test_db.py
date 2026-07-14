import urllib.request
import re
import json

req = urllib.request.Request('https://www.dramabox.com/video/41000102839_A-Breath-Away-From-Forever/568203144_Episode-1', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
    if match:
        data = json.loads(match.group(1))
        # save to db_next_data.json
        with open('db_next_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print("Saved to db_next_data.json")
except Exception as e:
    print(e)
