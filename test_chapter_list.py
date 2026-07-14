import requests

url = "https://www.reelshort.com/api/video/book/getChapterList"
payload = {
    "book_id": "6a3ba36a54aeacec4308eee8",
    "language": "en"
}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

resp = requests.post(url, json=payload, headers=headers)
print(resp.status_code, resp.text)
