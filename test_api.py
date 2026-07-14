import requests
import json

book_id = "6a3ba36a54aeacec4308eee8"
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*'
})

endpoints = [
    f"https://www.reelshort.com/api/video/book/chapter_list?book_id={book_id}",
    f"https://www.reelshort.com/api/video/book/getChapterList?book_id={book_id}",
    f"https://www.reelshort.com/api/video/chapter/list?book_id={book_id}",
    f"https://www.reelshort.com/api/book/{book_id}/chapters",
    f"https://www.reelshort.com/api/video/book/detail?book_id={book_id}",
    f"https://www.reelshort.com/api/video/book/getDetail?book_id={book_id}"
]

for url in endpoints:
    try:
        resp = session.get(url, timeout=5)
        if resp.status_code == 200:
            print(f"Success for {url}")
            print(str(resp.text)[:200])
        else:
            print(f"Failed {url} - {resp.status_code}")
    except Exception as e:
        print(f"Error {url}: {e}")
