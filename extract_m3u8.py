import requests
import re

html = requests.get('https://www.shorttv.live/episode/dubbed-reborn-as-the-villain-i-refuse-to-be-framed-27462-1').text
matches = re.findall(r'https?://[^"]+\.m3u8[^"]*', html)
print(matches[:5])
