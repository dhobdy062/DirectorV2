"""
Content models for session messages
"""

from typing import Optional, List, Union
from pydantic import BaseModel, ConfigDict
from .enums import ContentType, MsgStatus


class BaseContent(BaseModel):
    """Base content class for the content in the message."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        validate_default=True,
    )

    type: ContentType
    status: MsgStatus = MsgStatus.progress
    status_message: Optional[str] = None
    agent_name: Optional[str] = None


class TextContent(BaseContent):
    """Text content model class for text content."""
    text: str = ""
    type: ContentType = ContentType.text


class VideoData(BaseModel):
    """Video data model class for video content."""
    stream_url: Optional[str] = None
    external_url: Optional[str] = None
    player_url: Optional[str] = None
    id: Optional[str] = None
    collection_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    length: Optional[Union[int, float]] = None
    error: Optional[str] = None


class VideoContent(BaseContent):
    """Video content model class for video content."""
    video: Optional[VideoData] = None
    type: ContentType = ContentType.video


class VideosContentUIConfig(BaseModel):
    """UI configuration for videos content."""
    columns: Optional[int] = 4


class VideosContent(BaseContent):
    """Videos content model class for videos content."""
    videos: Optional[List[VideoData]] = None
    ui_config: VideosContentUIConfig = VideosContentUIConfig()
    type: ContentType = ContentType.videos


class ImageData(BaseModel):
    """Image data model class for image content."""
    url: str
    name: Optional[str] = None
    description: Optional[str] = None
    id: Optional[str] = None
    collection_id: Optional[str] = None


class ImageContent(BaseContent):
    """Image content model class for image content."""
    image: Optional[ImageData] = None
    type: ContentType = ContentType.image


class ShotData(BaseModel):
    """Shot data model class for search results content."""
    search_score: Union[int, float]
    start: Union[int, float]
    end: Union[int, float]
    text: str


class SearchData(BaseModel):
    """Search data model class for search results content."""
    video_id: str
    video_title: Optional[str] = None
    stream_url: str
    duration: Union[int, float]
    shots: List[ShotData]


class SearchResultsContent(BaseContent):
    """Search results content model class."""
    search_results: Optional[List[SearchData]] = None
    type: ContentType = ContentType.search_results
