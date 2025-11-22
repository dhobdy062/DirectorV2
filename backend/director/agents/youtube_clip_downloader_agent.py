import logging
import asyncio
import os
from typing import List, Optional
from pathlib import Path

from pydantic import BaseModel, Field

from director.agents.base import BaseAgent, AgentResponse, AgentStatus
from director.core.session import Session, MsgStatus, TextContent
from director.tools.videodb_tool import VideoDBTool

logger = logging.getLogger(__name__)


class DownloadResult(BaseModel):
    film: str
    title: str
    url: str
    filename: str
    filepath: str
    filesize_mb: float
    duration: str


class YouTubeClipDownloaderAgent(BaseAgent):
    """
    Downloads the best YouTube clips (from your previous search) directly to your local machine.
    Perfect for offline editing in Premiere/DaVinci/Reaper.
    """

    def __init__(self, session: Session, **kwargs):
        self.agent_name = "youtube_clip_downloader"
        self.description = (
            "Downloads previously found YouTube clips to your local disk. "
            "Uses yt-dlp (best quality, with audio, no watermark). "
            "Ready for editing your weekly discussion video."
        )
        self.parameters = self.get_parameters()
        super().__init__(session=session, **kwargs)

        self.download_folder = os.getenv(
            "CLIPS_DOWNLOAD_FOLDER",
            str(Path.home() / "Downloads" / "film_clips"),
        )
        Path(self.download_folder).mkdir(parents=True, exist_ok=True)

    def run(
        self,
        clips: List[dict],
        format: str = "best",
        max_concurrent: int = 3,
    ) -> AgentResponse:
        """
        Download the provided clips using yt-dlp.

        Args:
            clips: List of clip dicts (must contain at least 'url' and 'film')
                   Usually comes from YouTubeFilmClipAgent output.
            format: "best" (recommended), "720p", "1080p", "4k", etc.
            max_concurrent: How many simultaneous downloads (3–5 is safe)

        Returns:
            AgentResponse with list of downloaded files
        """
        try:
            if not clips:
                raise ValueError("No clips provided to download.")

            self.output_message.actions.append(
                f"Downloading {len(clips)} clips using yt-dlp..."
            )

            progress = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.progress,
                status_message="Preparing downloader...",
            )
            self.output_message.content.append(progress)
            self.output_message.push_update()

            results = asyncio.run(
                self._download_all(
                    clips, format=format, max_concurrent=max_concurrent, progress=progress
                )
            )

            total_mb = sum(r.filesize_mb for r in results)
            progress.text = (
                f"Downloaded {len(results)} clips successfully!\n\n"
                f"Total size: {total_mb:.1f} MB\n"
                f"Saved to: {self.download_folder}\n\n"
                "Ready for editing!"
            )
            progress.status = MsgStatus.success
            progress.status_message = "All clips downloaded!"
            self.output_message.publish()

            vdb = VideoDBTool(collection_id=self.session.collection_id or "default")
            uploads = []
            thumbs = []
            for r in results:
                try:
                    with open(r.filepath, "rb") as fh:
                        uploaded = vdb.upload(
                            source=fh,
                            source_type="file",
                            media_type="video",
                            name=r.filename,
                        )
                    uploads.append(uploaded)
                    thumb = vdb.extract_frame(uploaded.get("id"), timestamp=5)
                    thumbs.append(thumb)
                except Exception:
                    continue

            return AgentResponse(
                status=AgentStatus.SUCCESS,
                message=f"Successfully downloaded {len(results)} clips.",
                data={
                    "downloaded": [r.model_dump() for r in results],
                    "total_count": len(results),
                    "total_size_mb": round(total_mb, 1),
                    "folder": self.download_folder,
                    "uploaded_videos": uploads,
                    "thumbnails": thumbs,
                },
            )

        except Exception as e:
            logger.exception("YouTubeClipDownloaderAgent failed")
            error_text = TextContent(
                agent_name=self.agent_name,
                status=MsgStatus.error,
                status_message="Download failed. Is yt-dlp installed? (`pip install yt-dlp`)",
            )
            self.output_message.content.append(error_text)
            self.output_message.publish()

            return AgentResponse(
                status=AgentStatus.ERROR,
                message=f"Download failed: {str(e)}",
                data={},
            )

    async def _download_all(self, clips, format: str, max_concurrent: int, progress: TextContent):
        import yt_dlp

        def sanitize_filename(name: str) -> str:
            return "".join(c if c.isalnum() or c in " _-()" else "_" for c in name)[:100]

        semaphore = asyncio.Semaphore(max_concurrent)
        results = []

        async def download_one(clip: dict, index: int):
            async with semaphore:
                url = clip["url"]
                film = clip.get("film", "Unknown_Film")
                title = clip.get("title", "Unknown_Title")

                safe_name = sanitize_filename(f"{film} - {title}")
                output_path = str(Path(self.download_folder) / f"{safe_name}.%(ext)s")

                ydl_opts = {
                    "format": {
                        "best": "bestvideo+bestaudio/best",
                        "720p": "best[height<=720]+bestaudio/best",
                        "1080p": "best[height<=1080]+bestaudio/best",
                        "4k": "best[height<=2160]+bestaudio/best",
                    }.get(format, "best"),
                    "merge_output_format": "mp4",
                    "outtmpl": output_path,
                    "quiet": True,
                    "no_warnings": True,
                    "continuedl": True,
                    "retries": 10,
                }

                progress.status_message = f"Downloading ({index+1}/{len(clips)}): {film}"
                self.output_message.push_update()

                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        filepath = Path(filename)

                        results.append(
                            DownloadResult(
                                film=film,
                                title=title,
                                url=url,
                                filename=filepath.name,
                                filepath=str(filepath),
                                filesize_mb=filepath.stat().st_size / (1024 * 1024),
                                duration=info.get("duration_string", "Unknown"),
                            )
                        )
                except Exception as e:
                    logger.error(f"Failed to download {url}: {e}")

        tasks = [download_one(clip, i) for i, clip in enumerate(clips)]
        await asyncio.gather(*tasks)

        return results