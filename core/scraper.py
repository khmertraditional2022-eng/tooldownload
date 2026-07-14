import json
import urllib.request
import re
import math
import requests
from bs4 import BeautifulSoup

def get_chapter_list(book_id):
    episodes = []
    page = 1
    page_size = 100
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    while True:
        api_url = f"https://www.reelshort.com/api/video/book/getChapterList?book_id={book_id}&language=en&page={page}&page_size={page_size}"
        try:
            import time
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    req = urllib.request.Request(api_url, headers=headers)
                    with urllib.request.urlopen(req, timeout=10) as response:
                        data = json.loads(response.read().decode('utf-8'))
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(2)
                
            if data.get('code') != 0:
                break
                
            chapter_list = data.get('data', {}).get('chapter_list', [])
            if not chapter_list:
                break
                
            book_title = data.get('data', {}).get('book_title', 'Video')
                
            for chap in chapter_list:
                chapter_id = chap['chapter_id']
                serial = chap['serial_number']
                ep_url = f"https://www.reelshort.com/episodes/episode-{serial}-vid-{book_id}-{chapter_id}"
                
                episodes.append({
                    'title': f"Episode {serial} - {book_title}",
                    'url': ep_url,
                    'stream_url': None,
                    'platform': 'ReelShort',
                    'status': 'Ready'
                })
                
            if len(chapter_list) < page_size:
                break
            page += 1
            
        except Exception as e:
            print(f"ReelShort API Fetch Error: {e}")
            break
            
    return episodes

def scrape_dramabox(url):
    episodes = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Extract bookId from url, usually an 11-digit number
    # e.g., video/41000102839_A-Breath-Away-From-Forever/
    match = re.search(r'(\d{10,13})', url)
    if not match:
        print("DramaBox: Could not find bookId in URL")
        return []
        
    book_id = match.group(1)
    api_url = f"https://api.sansekai.my.id/api/dramabox/allepisode?bookId={book_id}"
    
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        if isinstance(data, list):
            for chap in data:
                ep_name = chap.get('chapterName', '')
                index = chap.get('chapterIndex', 0)
                
                # Check for direct mp4 url
                stream_url = None
                cdn_list = chap.get('cdnList', [])
                if cdn_list and len(cdn_list) > 0:
                    video_paths = cdn_list[0].get('videoPathList', [])
                    if video_paths and len(video_paths) > 0:
                        stream_url = video_paths[0].get('videoPath')
                
                # Construct fallback dummy URL for UI display and fallback yt-dlp handling
                chapter_id = chap.get('chapterId', '0')
                ep_url = f"https://www.dramabox.com/video/{book_id}_drama/{chapter_id}_ep"
                
                # If stream_url is available, we pass it as the actual url to download
                download_url = stream_url if stream_url else ep_url
                
                episodes.append({
                    "title": f"Episode {index} - {ep_name}",
                    "url": download_url,
                    "stream_url": stream_url,
                    "platform": "DramaBox",
                    "status": "Ready"
                })
                
        # If extraction failed, fallback to the provided URL
        if not episodes:
            episodes.append({
                "title": "DramaBox Video",
                "url": url,
                "stream_url": None,
                "platform": "DramaBox",
                "status": "Ready"
            })
            
    except Exception as e:
        print(f"DramaBox API Scrape Error: {e}")
        
    return episodes

def scrape_sansekai_dramabox(url):
    episodes = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    match = re.search(r'(\d{8,15})', url)
    if not match:
        print("DramaBox: Could not find bookId in URL")
        return []
        
    book_id = match.group(1)
    api_url = f"https://api.sansekai.my.id/api/dramabox/allepisode?bookId={book_id}"
    
    try:
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                req = urllib.request.Request(api_url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    data = json.loads(response.read().decode('utf-8'))
                break # Success, exit retry loop
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(2)
            
        if isinstance(data, list):
            for chap in data:
                ep_name = chap.get('chapterName', '')
                index = chap.get('chapterIndex', 0)
                
                stream_url = None
                cdn_list = chap.get('cdnList', [])
                if cdn_list and len(cdn_list) > 0:
                    video_paths = cdn_list[0].get('videoPathList', [])
                    if video_paths and len(video_paths) > 0:
                        stream_url = video_paths[0].get('videoPath')
                
                download_url = stream_url if stream_url else url
                
                episodes.append({
                    "title": f"Episode {index} - {ep_name}",
                    "url": download_url,
                    "stream_url": stream_url,
                    "platform": "DramaBox",
                    "status": "Ready"
                })
    except Exception as e:
        print(f"DramaBox API Scrape Error: {e}")
        
    return episodes

def scrape_episodes(url_input, platform="Unknown"):
    """
    Scrape all episodes based on the selected platform.
    """
    all_episodes = []
    urls = [u.strip() for u in re.split(r'[\n,]', url_input) if u.strip().startswith('http')]
    
    for url in urls:
        if platform == "DramaBox" or "dramabox" in url.lower():
            eps = scrape_sansekai_dramabox(url)
            if eps:
                all_episodes.extend(eps)
                continue
                
        if platform == "ReelShort" or "reelshort" in url.lower():
            match = re.search(r'-([a-f0-9]{24})(?:-[a-z0-9]+)?(?:[/?]|$)', url)
            if match:
                book_id = match.group(1)
                eps = get_chapter_list(book_id)
                if eps:
                    all_episodes.extend(eps)
                    continue
                    
        # If no specific scraper works or platform not fully supported, fallback to single generic download
        all_episodes.append({
            'title': f"{platform} Video",
            'url': url,
            'stream_url': None,
            'platform': platform,
            'status': 'Ready'
        })
            
    return all_episodes
