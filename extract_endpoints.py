import requests
import re
import json

html = requests.get('https://api.sansekai.my.id/').text
matches = re.findall(r'"(/[^"]+)":\s*\{\s*get:\s*\{[^}]+parameters:\s*\[(.*?)\]', html, re.DOTALL)
for m in matches:
    if 'reelshort' in m[0] or 'shortmax' in m[0] or 'pinedrama' in m[0] or 'freereels' in m[0] or 'dramabox' in m[0]:
        print("Endpoint:", m[0])
        print("Params:", re.findall(r'name:\s*"([^"]+)"', m[1]))
