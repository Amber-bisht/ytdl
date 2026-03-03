# 🎬 YouTube Playlist Downloader & Uploader Bot

A Telegram bot that downloads YouTube videos/playlists in **1080p** and uploads them directly to your chat. Built with [Pyrogram](https://docs.pyrogram.org/) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

> Made by [Amber Bisht](https://amberbisht.me)

---

## ✨ Features

- 📥 **Download YouTube videos & playlists** in up to 1080p MP4
- 📤 **Auto-upload to Telegram** with thumbnails and captions
- 🔢 **Range selection** — download specific videos from a playlist (e.g., videos 5–20)
- 📋 **Playlist indexing** — list all videos with their index before downloading
- ✂️ **Auto-split** — videos exceeding Telegram's 2 GB limit are automatically split
- 🍪 **Cookie support** — bypass age-restricted or region-locked videos
- 🛑 **Cancellable downloads** — abort mid-playlist with `/cancel`
- 🔄 **Fallback strategies** — multiple `player_client` fallbacks to handle YouTube 403 errors
- 🐳 **Dockerized** with CI/CD via GitHub Actions

---

## 🤖 Bot Commands

| Command | Description |
|---|---|
| `/start` | Show welcome message and usage instructions |
| `/index <url>` | List all videos in a playlist with index numbers |
| `/ytdl <url> [start-end]` | Download playlist or single video. Optional range. |
| `/cancel` | Abort the current download operation |
| `/cookies <json>` | Set YouTube cookies (JSON array or Netscape file) |

### Examples

```
/ytdl https://www.youtube.com/watch?v=dQw4w9WgXcQ

/ytdl https://www.youtube.com/playlist?list=PLxxxxxx 1-10

/index https://www.youtube.com/playlist?list=PLxxxxxx
```

---

## 🛠️ Tech Stack

- **Python 3.12+**
- **Pyrogram** — Telegram MTProto API client
- **yt-dlp** — YouTube downloader
- **FFmpeg** — video processing & splitting
- **Deno** — JavaScript runtime for yt-dlp's n-challenge solver
- **Docker** — containerized deployment

---

## 🚀 Setup

### Prerequisites

- Python 3.12+
- FFmpeg
- [Deno](https://deno.land/) (required for yt-dlp to solve YouTube's JS challenges)
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)
- A Bot Token from [@BotFather](https://t.me/BotFather)

### Local Setup

```bash
# Clone the repo
git clone https://github.com/Amber-bisht/ytdl-uploader-bot.git
cd ytdl-uploader-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API_ID, API_HASH, and BOT_TOKEN

# Run
python bot.py
```

### Docker Setup

```bash
docker build -t ytdl-bot .
docker run -d --name ytdl-bot \
  -p 6666:6666 \
  --env-file .env \
  --restart unless-stopped \
  ytdl-bot
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
```

---

## 📁 Project Structure

```
├── bot.py             # Telegram bot handlers & commands
├── downloader.py      # yt-dlp download logic with fallback strategies
├── splitter.py        # FFmpeg-based video splitting for Telegram's 2GB limit
├── test_dl.py         # Test script to verify download strategies
├── cookies.txt        # YouTube cookies (Netscape format, gitignored)
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container config with Python, FFmpeg, Deno
└── .github/workflows/
    └── deploy.yml     # CI/CD pipeline — auto-deploy on push to main
```

---

## 🔐 Cookie Setup

For age-restricted or login-required videos:

1. Install a browser extension like **"Get cookies.txt LOCALLY"**
2. Export cookies from youtube.com
3. Send the cookies to the bot using:
   - `/cookies` with JSON array pasted as text
   - `/cookies` as caption on an uploaded `.txt` file
   - Reply to a cookie file with `/cookies`

---

## 🚢 Deployment

This project includes a **GitHub Actions CI/CD pipeline** that automatically:

1. Builds the Docker image
2. Pushes to GitHub Container Registry (GHCR)
3. Deploys to your server via SSH

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `SERVER_HOST` | Server IP or hostname |
| `SERVER_USER` | SSH username |
| `SERVER_PASSWORD` | SSH password |
| `ENV_FILE` | Contents of the `.env` file |

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ by <a href="https://amberbisht.me">Amber Bisht</a>
</p>
