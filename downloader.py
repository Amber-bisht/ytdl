import os
import asyncio
from typing import List, Dict, Any
import yt_dlp

def extract_playlist_info(url: str) -> List[Dict[str, Any]]:
    """Extract information for all videos in a playlist without downloading."""
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'extractor_args': {'youtube': {'player_client': ['ios']}},
    }
    
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = "cookies.txt"
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            return info['entries']
        return [info] # It might be a single video, not a playlist

def download_video(url: str, output_dir: str = ".") -> Dict[str, Any]:
    """Download a single video in 1080p and its thumbnail, returning metadata."""
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'writethumbnail': True,
        'postprocessors': [{'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'}],
        'quiet': True,
        'no_warnings': True,
        'nopart': True,
        'geo_bypass': True,
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg' if os.path.exists('/opt/homebrew/bin/ffmpeg') else None,
        'nocheckcertificate': True,
        'extractor_args': {'youtube': {'player_client': ['ios']}},
    }
    
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = "cookies.txt"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return {
            'id': info.get('id'),
            'title': info.get('title'),
            'description': info.get('description'),
            'file_path': ydl.prepare_filename(info),
            'thumb_path': os.path.join(output_dir, f"{info.get('id')}.jpg"),
            'duration': info.get('duration')
        }

async def async_extract_playlist_info(url: str):
    return await asyncio.to_thread(extract_playlist_info, url)

async def async_download_video(url: str, output_dir: str = "."):
    return await asyncio.to_thread(download_video, url, output_dir)
