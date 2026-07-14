import yt_dlp
url = 'https://akamai-static.shorttv.live/hls-encrypted/7befb98627e84eb39c73eba0a96ace0f_720/main.m3u8?auth_key=1783874849-0-0-fc4966e8b1d9ff0a7cc0164fba07ed29'
ydl_opts = {'verbose': True}
ydl = yt_dlp.YoutubeDL(ydl_opts)
info = ydl.extract_info(url, download=False)
for f in info.get('formats', []):
    print(f.get('format_id'), f.get('vcodec'), f.get('acodec'))
