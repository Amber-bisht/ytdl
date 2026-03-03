FROM python:3.12-slim

# Install system dependencies (ffmpeg + deno requirements)
RUN apt-get update && \
    apt-get install -y ffmpeg curl unzip gcc libc6-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Deno (required by yt-dlp for YouTube n-challenge solving)
RUN curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the defined port
EXPOSE 6666

# Run the bot
CMD ["python", "bot.py"]
