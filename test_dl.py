"""
Test script for YouTube downloads.
Tries multiple player_client strategies as fallbacks to avoid 403 errors.
Run: python test_dl.py
"""
import yt_dlp
import sys
import os
import shutil

TEST_URL = "https://www.youtube.com/watch?v=0bHoB32fuj0"

# Ordered list of player_client fallback strategies (best → last resort)
STRATEGIES = [
    {
        "name": "default (let yt-dlp decide)",
        "player_client": None,  # Don't override — use yt-dlp's built-in default
    },
    {
        "name": "web_safari",
        "player_client": ["web_safari"],
    },
    {
        "name": "web_embedded + web",
        "player_client": ["web_embedded", "web"],
    },
    {
        "name": "mweb + web",
        "player_client": ["mweb", "web"],
    },
]

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def clear_cache():
    """Remove yt-dlp cache to avoid stale data."""
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "yt-dlp")
    if os.path.isdir(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)
        print("  [*] Cache cleared")


def build_opts(strategy, download=False):
    """Build yt-dlp options for a given strategy."""
    opts = {
        "format": (
            "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/"
            "bestvideo[height<=1080]+bestaudio/"
            "best[height<=1080]/best"
        ),
        "outtmpl": os.path.join("test_downloads", "%(id)s.%(ext)s"),
        "quiet": False,
        "verbose": True,
        "no_warnings": False,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "check_formats": "selected",
        "cachedir": False,
        "http_headers": {"User-Agent": USER_AGENT},
        "remote_components": {"ejs:github": True},
    }

    if os.path.exists("cookies.txt"):
        opts["cookiefile"] = "cookies.txt"

    if strategy["player_client"] is not None:
        opts["extractor_args"] = {
            "youtube": {"player_client": strategy["player_client"]}
        }

    return opts


def test_extract(strategy):
    """Test metadata extraction (no download) — fast check for 403."""
    print(f"\n{'='*60}")
    print(f"  Strategy: {strategy['name']}")
    print(f"  Mode: EXTRACT ONLY (no download)")
    print(f"{'='*60}")
    clear_cache()
    opts = build_opts(strategy, download=False)
    opts["quiet"] = True
    opts["verbose"] = False

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(TEST_URL, download=False)
            title = info.get("title", "???")
            formats_count = len(info.get("formats", []))
            print(f"  ✅ Extract OK — \"{title}\" ({formats_count} formats)")
            return True
    except Exception as e:
        print(f"  ❌ Extract FAILED — {e}")
        return False


def test_download(strategy):
    """Test actual download — full verification."""
    print(f"\n{'='*60}")
    print(f"  Strategy: {strategy['name']}")
    print(f"  Mode: FULL DOWNLOAD")
    print(f"{'='*60}")
    clear_cache()
    os.makedirs("test_downloads", exist_ok=True)
    opts = build_opts(strategy, download=True)

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(TEST_URL, download=True)
            filepath = ydl.prepare_filename(info)
            if os.path.exists(filepath):
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f"  ✅ Download OK — {filepath} ({size_mb:.1f} MB)")
                os.remove(filepath)  # Cleanup
                return True
            else:
                print(f"  ❌ Download FAILED — file not found at {filepath}")
                return False
    except Exception as e:
        print(f"  ❌ Download FAILED — {e}")
        return False


def main():
    print(f"yt-dlp version: {yt_dlp.version.__version__}")
    print(f"Test URL: {TEST_URL}")

    # Phase 1: Quick extract test across all strategies
    print("\n" + "=" * 60)
    print("  PHASE 1: Testing metadata extraction (fast)")
    print("=" * 60)

    working_strategies = []
    for strategy in STRATEGIES:
        if test_extract(strategy):
            working_strategies.append(strategy)

    if not working_strategies:
        print("\n❌ ALL strategies failed extraction. Check cookies / yt-dlp version.")
        sys.exit(1)

    # Phase 2: Full download test with first working strategy
    print("\n" + "=" * 60)
    print("  PHASE 2: Testing full download with working strategies")
    print("=" * 60)

    for strategy in working_strategies:
        if test_download(strategy):
            print(f"\n🎉 SUCCESS — Use strategy: {strategy['name']}")
            if strategy["player_client"]:
                print(f"   player_client: {strategy['player_client']}")
            else:
                print("   player_client: (use yt-dlp default, no override needed)")

            # Cleanup test_downloads dir
            shutil.rmtree("test_downloads", ignore_errors=True)
            sys.exit(0)

    print("\n❌ All strategies passed extraction but failed download.")
    print("   Cookies may be expired — try re-exporting them.")
    shutil.rmtree("test_downloads", ignore_errors=True)
    sys.exit(1)


if __name__ == "__main__":
    main()
