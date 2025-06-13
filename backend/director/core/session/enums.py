"""
Enums for session management
"""

from enum import Enum


class RoleTypes(str, Enum):
    """Role types for the context message."""
    system = "system"
    user = "user"
    assistant = "assistant"
    tool = "tool"


class MsgStatus(str, Enum):
    """Message status for the message, for loading state."""
    progress = "progress"
    success = "success"
    error = "error"
    not_generated = "not_generated"
    overlimit = "overlimit"
    sessionlimit = "sessionlimit"


class MsgType(str, Enum):
    """Message type for the message. input is for the user input and output is for the director output."""
    input = "input"
    output = "output"


class ContentType(str, Enum):
    """Content type for the content in the input/output message."""
    text = "text"
    video = "video"
    videos = "videos"
    image = "image"
    search_results = "search_results"


class EventType(str, Enum):
    """Event types for WebSocket event emission."""
    update_data = "update_data"
