"""
Session management package

This package contains the refactored session management components
split into multiple modules for better maintainability.
"""

from .enums import RoleTypes, MsgStatus, MsgType, ContentType, EventType
from .events import BaseEvent, CollectionsUpdateEvent, VideosUpdateEvent
from .content import (
    BaseContent, TextContent, VideoData, VideoContent, 
    VideosContent, VideosContentUIConfig, ImageData, ImageContent,
    ShotData, SearchData, SearchResultsContent
)
from .messages import BaseMessage, InputMessage, OutputMessage, ContextMessage, format_user_message
from .session import Session

__all__ = [
    # Enums
    "RoleTypes", "MsgStatus", "MsgType", "ContentType", "EventType",
    # Events
    "BaseEvent", "CollectionsUpdateEvent", "VideosUpdateEvent",
    # Content
    "BaseContent", "TextContent", "VideoData", "VideoContent",
    "VideosContent", "VideosContentUIConfig", "ImageData", "ImageContent",
    "ShotData", "SearchData", "SearchResultsContent",
    # Messages
    "BaseMessage", "InputMessage", "OutputMessage", "ContextMessage", "format_user_message",
    # Session
    "Session"
]
