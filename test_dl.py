import yt_dlp
import sys

ydl_opts = {
    'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
    'extractor_args': {'youtube': {'player_client': ['ios', 'web']}},
    'cookiefile': 'cookies.txt',
    'verbose': True
}
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("https://www.youtube.com/watch?v=0bHoB32fuj0", download=False)
        print("Success")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
