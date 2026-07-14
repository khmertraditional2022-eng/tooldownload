import yt_dlp
import os
import re

def clean_filename(title):
    # Remove invalid characters for filenames
    return re.sub(r'[\\/*?:"<>|\n\r\t]', "", title).strip()

def download_episode(url, title, output_dir, progress_callback=None, yt_mode=0):
    """
    Download video using yt-dlp.
    yt_mode: 0=Single, 1=Playlist, 2=Audio
    """
    safe_title = clean_filename(title)
    
    if yt_mode == 1:
        # For playlist, put inside a folder and number them
        output_template = os.path.join(output_dir, "%(playlist_title)s", "%(playlist_index)s - %(title)s.%(ext)s")
    else:
        if "youtube" in url.lower() or "youtu.be" in url.lower():
            output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
        else:
            output_template = os.path.join(output_dir, f"{safe_title}.%(ext)s")
    
    def my_hook(d):
        if d['status'] == 'downloading':
            try:
                # Remove ANSI escape codes from percentage
                percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d['_percent_str']).strip()
                percent = float(percent_str.replace('%', ''))
                if progress_callback:
                    progress_callback(int(percent))
            except Exception:
                pass
        elif d['status'] == 'finished':
            if progress_callback:
                progress_callback(100)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [my_hook],
        'extract_flat': False,
        'compat_opts': {'no-file-urls'},
    }
    
    if yt_mode == 0:
        ydl_opts['noplaylist'] = True
    elif yt_mode == 1:
        ydl_opts['yesplaylist'] = True
    elif yt_mode == 2:
        ydl_opts['noplaylist'] = True
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    # Check if cookies.txt exists in the app data folder
    cookie_path = os.path.join(os.path.expanduser("~"), ".downloadreel", "cookies.txt")
    if os.path.exists(cookie_path):
        ydl_opts['cookiefile'] = cookie_path
    else:
        # Fallback
        fallback_cookie = os.path.join(os.getcwd(), "cookies.txt")
        if os.path.exists(fallback_cookie):
            ydl_opts['cookiefile'] = fallback_cookie

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Download failed for {url}: {e}")
        return False
