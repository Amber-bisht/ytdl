import os
import asyncio
import shutil
import logging
from typing import List, Dict, Any
import yt_dlp

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# Ordered fallback strategies for player_client
PLAYER_CLIENT_STRATEGIES = [
    None,                        # Use yt-dlp default
    ["web_safari"],
    ["web_embedded", "web"],
    ["mweb", "web"],
]

def _clear_cache():
    """Remove yt-dlp cache to avoid stale data."""
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "yt-dlp")
    if os.path.isdir(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _base_opts() -> dict:
    """Common options shared across all yt-dlp calls."""
    opts = {
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'cachedir': False,
        'http_headers': {'User-Agent': USER_AGENT},
        'remote_components': {'ejs:github': True},
    }
    if os.path.exists("cookies.txt"):
        opts['cookiefile'] = "cookies.txt"
    return opts


def extract_playlist_info(url: str) -> List[Dict[str, Any]]:
    """Extract information for all videos in a playlist without downloading."""
    ydl_opts = _base_opts()
    ydl_opts['extract_flat'] = True

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            return info['entries']
        return [info]  # It might be a single video, not a playlist

def download_video(url: str, output_dir: str = ".") -> Dict[str, Any]:
    """Download a single video in 1080p and its thumbnail, returning metadata.
    
    Tries multiple player_client strategies as fallbacks to handle 403 errors.
    """
    os.makedirs(output_dir, exist_ok=True)
    _clear_cache()

    last_error = None
    for strategy in PLAYER_CLIENT_STRATEGIES:
        ydl_opts = _base_opts()
        ydl_opts.update({
            'format': (
                'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/'
                'bestvideo[height<=1080]+bestaudio/'
                'best[height<=1080]/best'
            ),
            'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
            'writethumbnail': True,
            'postprocessors': [{'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'}],
            'nopart': True,
            'check_formats': 'selected',
            'ffmpeg_location': '/opt/homebrew/bin/ffmpeg' if os.path.exists('/opt/homebrew/bin/ffmpeg') else None,
        })

        if strategy is not None:
            ydl_opts['extractor_args'] = {
                'youtube': {'player_client': strategy}
            }
            logger.info(f"Trying player_client: {strategy}")
        else:
            logger.info("Trying default player_client")

        try:
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
        except Exception as e:
            last_error = e
            logger.warning(f"Strategy {strategy or 'default'} failed: {e}")
            continue

    # All strategies failed
    raise last_error or Exception("All download strategies failed")

async def async_extract_playlist_info(url: str):
    return await asyncio.to_thread(extract_playlist_info, url)

async def async_download_video(url: str, output_dir: str = "."):
    return await asyncio.to_thread(download_video, url, output_dir)
