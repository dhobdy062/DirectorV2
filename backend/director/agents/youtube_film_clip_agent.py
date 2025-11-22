import os
import logging
import httpx
import asyncio
from typing import List

from pydantic import BaseModel, Field

from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import Session, MsgStatus, TextContent

logger = logging.getLogger(__name__)


class FilmClip(BaseModel):
    film: str
    title: str
    channel: str
    duration: str
    views: int
    url: str
    embed_url: str
    thumbnail: str


class YouTubeFilmClipAgent(BaseAgent):
    """
    Finds the best discussion-worthy YouTube clips (scenes, video essays, supercuts, analysis)
    for a list of films — perfect for your weekly "Best Films" discussion videos.
    """

    def __init__(self, session: Session, **kwargs):
        self.agent_name = "youtube_film_clips"
        self.description = (
            "Finds high-quality, fair-use-friendly YouTube clips (scenes, analysis, supercuts, video essays) "
            "for any list of films. Ideal for weekly discussion episodes."
        )
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY must be set in environment")

        self.http = httpx.AsyncClient(timeout=30.0)

    def run(self, films: List[str], max_per_film: int = 3) -> AgentResponse:
        """
        Search for the best clips for each film.

        Args:
            films: List of movie titles (e.g. ["Pulp Fiction", "The Godfather"])
            max_per_film: Number of top clips to return per film (default: 3)

        Returns:
            AgentResponse with list of rich clip data ready for video production
        """
        try:
            if not films or not isinstance(films, list):
                raise ValueError("Please provide a non-empty list of film titles.")

            self.output_message.actions.append("Starting YouTube clip search...")
            progress_text = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.progress,
                status_message=f"Searching clips for {len(films)} films...",
            )
            self.output_message.content.append(progress_text)
            self.output_message.push_update()

            clips = asyncio.run(self._search_all_clips(films, max_per_film, progress_text))

            progress_text.text = (
                f"Found {len(clips)} amazing clips!\n\n"
                "Ready for your weekly discussion video. "
                "You can now copy embed links or download via yt-dlp."
            )
            progress_text.status = MsgStatus.success
            progress_text.status_message = "Clip search completed successfully!"
            self.output_message.publish()

            return AgentResponse(
                status=AgentStatus.SUCCESS,
                message=f"Found {len(clips)} high-quality clips for your discussion.",
                data={
                    "clips": [clip.model_dump() for clip in clips],
                    "total": len(clips),
                    "films_searched": films,
                },
            )

        except Exception as e:
            logger.exception("YouTubeFilmClipAgent failed")
            error_text = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.error,
                status_message="Failed to find clips. Check your API key or internet connection.",
            )
            self.output_message.content.append(error_text)
            self.output_message.publish()

            return AgentResponse(
                status=AgentStatus.ERROR,
                message=f"YouTube clip search failed: {str(e)}",
                data={},
            )

    async def _search_all_clips(self, films: List[str], max_per_film: int, progress_text: TextContent):
        all_clips = []

        for i, film in enumerate(films):
            progress_text.status_message = f"Searching clips for: {film} ({i+1}/{len(films)})"
            self.output_message.push_update()

            clips = await self._search_clips_for_film(film, max_per_film * 2)
            all_clips.extend(clips[:max_per_film])

            await asyncio.sleep(0.3)

        return all_clips

    async def _search_clips_for_film(self, film: str, limit: int) -> List[FilmClip]:
        queries = [
            f"{film} best scenes",
            f"{film} video essay",
            f"{film} supercut",
            f"{film} analysis breakdown",
            f"{film} all scenes",
            f"{film} montage",
            f"{film} explained ending",
        ]

        candidates = []

        for query in queries:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": 8,
                "videoEmbeddable": "true",
                "order": "viewCount",
                "key": self.api_key,
            }

            try:
                r = await self.http.get(url, params=params)
                r.raise_for_status()
                items = r.json().get("items", [])

                video_ids = [item["id"]["videoId"] for item in items]
                if not video_ids:
                    continue

                details = await self.http.get(
                    "https://www.googleapis.com/youtube/v3/videos",
                    params={
                        "part": "contentDetails,statistics,snippet",
                        "id": ",".join(video_ids),
                        "key": self.api_key,
                    },
                )
                details.raise_for_status()
                for video in details.json().get("items", []):
                    stats = video.get("statistics", {})
                    duration = video.get("contentDetails", {}).get("duration", "")
                    snippet = video.get("snippet", {})

                    title = snippet.get("title", "").lower()
                    if any(t in title for t in ["trailer", "teaser", "official trailer"]):
                        continue
                    if not self._is_good_clip_duration(duration):
                        continue

                    views = int(stats.get("viewCount", 0))
                    vid = video.get("id", "")

                    candidates.append(
                        FilmClip(
                            film=film,
                            title=snippet.get("title", ""),
                            channel=snippet.get("channelTitle", ""),
                            duration=duration,
                            views=views,
                            url=f"https://www.youtube.com/watch?v={vid}",
                            embed_url=f"https://www.youtube.com/embed/{vid}",
                            thumbnail=snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                        )
                    )

            except Exception as e:
                logger.warning(f"Query failed: {query} → {e}")

        candidates.sort(key=lambda x: x.views, reverse=True)
        return candidates[:limit]

    def _is_good_clip_duration(self, iso: str) -> bool:
        if not iso.startswith("PT"):
            return False
        time_str = iso[2:]
        minutes = 0
        seconds = 0
        if "M" in time_str:
            minutes = int(time_str.split("M")[0])
            time_str = time_str.split("M")[1]
        if "S" in time_str:
            seconds = int(time_str[:-1])
        total_minutes = minutes + seconds / 60
        return 1.5 <= total_minutes <= 20.0