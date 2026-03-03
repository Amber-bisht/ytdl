import os
import math
import asyncio
from typing import List

MAX_SIZE = 1.95 * 1024 * 1024 * 1024  # 1.95 GB to be safe against Telegram's 2GB limit

async def split_video(file_path: str, duration: int) -> List[str]:
    """
    Splits a video file if it exceeds the MAX_SIZE limit.
    Returns a list of file paths (either the original if no split, or the split parts).
    """
    size = os.path.getsize(file_path)
    if size <= MAX_SIZE:
        return [file_path]
    
    parts = math.ceil(size / MAX_SIZE)
    # Give a bit of overlap or just integer division for chunk_duration
    chunk_duration = math.ceil(duration / parts)
    
    output_files = []
    base_name, ext = os.path.splitext(file_path)
    
    for i in range(parts):
        start_time = i * chunk_duration
        output_file = f"{base_name}_part{i+1}{ext}"
        output_files.append(output_file)
        
        # Using ffmpeg to split. -c copy is fast but might not cut exactly on keyframes.
        # However, for pure splitting to bypass size limits, it's usually acceptable.
        cmd = [
            "ffmpeg",
            "-y", # Overwrite if exists
            "-i", file_path,
            "-ss", str(start_time),
            "-t", str(chunk_duration),
            "-c", "copy",
            output_file
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        
    return output_files
