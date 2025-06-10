import os
from yt_dlp import YoutubeDL, DownloadError
from app.config import settings

def download_audio(video_url: str) -> str:
    """
    Downloads the best audio from `video_url` into settings.download_dir
    and returns the path to the .mp3 file.
    """
    os.makedirs(settings.download_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{settings.download_dir}/%(id)s.%(ext)s',
        'keepvideo': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': settings.audio_format,
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            return f"{base}.{settings.audio_format}"
    except DownloadError as e:
        raise RuntimeError(f"Audio download failed: {e}")
