import requests

url = "https://dramabox.sansekai.my.id/api/dramabox/allepisode?bookId=71000"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0 Safari/537.36'}
try:
    resp = requests.get(url, headers=headers, timeout=10)
    print(resp.status_code)
    print(resp.text[:500])
except Exception as e:
    print(e)
