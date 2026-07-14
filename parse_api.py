import requests
import re
html = requests.get('https://api.sansekai.my.id/').text
paths = re.findall(r'"(/[a-z-]+/allepisode)"', html)
print("allepisode paths:", paths)
paths = re.findall(r'"(/[a-z-]+/get-download-url)"', html)
print("download paths:", paths)
