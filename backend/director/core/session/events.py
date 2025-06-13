"""
Event classes for WebSocket communication
"""

from pydantic import BaseModel
from .enums import EventType


class BaseEvent(BaseModel):
    """Base event class for the WebSocket event."""
    event_type: EventType


class CollectionsUpdateEvent(BaseEvent):
    """Collections update event class for the WebSocket event."""
    event_type: EventType = EventType.update_data
    update: str = "collections"


class VideosUpdateEvent(BaseEvent):
    """Videos update event class for the WebSocket event."""
    event_type: EventType = EventType.update_data
    update: str = "videos"
    collection_id: str
