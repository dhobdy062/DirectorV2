"""
YouTube related agents registry
"""

from director.agents.youtube_film_clip_agent import YouTubeFilmClipAgent
from director.agents.youtube_clip_downloader_agent import YouTubeClipDownloaderAgent

YOUTUBE_AGENTS = [
    YouTubeFilmClipAgent,
    YouTubeClipDownloaderAgent,
]