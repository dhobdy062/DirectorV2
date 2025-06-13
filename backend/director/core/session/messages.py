"""
Message classes for session communication
"""

import json
from datetime import datetime
from typing import Optional, List, Union
from pydantic import BaseModel, Field, ConfigDict
from flask_socketio import emit

from director.db.base import BaseDB
from .enums import RoleTypes, MsgStatus, MsgType
from .content import (
    TextContent, ImageContent, VideoContent, 
    VideosContent, SearchResultsContent
)


def format_user_message(message: dict) -> dict:
    """Format user message content for processing"""
    message_content = message.get("content")
    if isinstance(message_content, str):
        return message
    else:
        content_parts = message["content"]
        sanitized_content_parts = []

        for content_part in content_parts:
            sanitized_part = content_part
            if content_part["type"] == "image":
                sanitized_part = {
                    "type": "text",
                    "text": f"User has upload image with following details : {json.dumps(content_part)}",
                }
            sanitized_content_parts.append(sanitized_part)

        message["content"] = sanitized_content_parts
        return message


class BaseMessage(BaseModel):
    """Base message class for the input/output message. All the input/output messages will be inherited from this class."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        validate_default=True,
    )

    session_id: str
    conv_id: str
    msg_type: MsgType
    actions: List[str] = []
    agents: List[str] = []
    content: List[
        Union[
            dict,
            TextContent,
            ImageContent,
            VideoContent,
            VideosContent,
            SearchResultsContent,
        ]
    ] = []
    status: MsgStatus = MsgStatus.success
    msg_id: str = Field(
        default_factory=lambda: str(datetime.now().timestamp() * 100000)
    )


class InputMessage(BaseMessage):
    """Input message from the user. This class is used to create the input message from the user."""
    db: BaseDB
    msg_type: MsgType = MsgType.input

    def publish(self):
        """Store the message in the database. for conversation history."""
        self.db.add_or_update_msg_to_conv(**self.model_dump(exclude={"db"}))


class OutputMessage(BaseMessage):
    """Output message from the director. This class is used to create the output message from the director."""
    db: BaseDB = Field(exclude=True)
    msg_type: MsgType = MsgType.output
    status: MsgStatus = MsgStatus.progress

    def update_status(self, status: MsgStatus):
        """Update the status of the message and publish the message to the socket. for loading state."""
        self.status = status
        self._publish()

    def push_update(self):
        """Publish the message to the socket."""
        try:
            self._publish()
        except Exception as e:
            print(f"Error in emitting message: {str(e)}")

    def publish(self):
        """Store the message in the database. for conversation history and publish the message to the socket."""
        self._publish()

    def _publish(self):
        try:
            emit("chat", self.model_dump(), namespace="/chat")
        except Exception as e:
            print(f"Error in emitting message: {str(e)}")
        self.db.add_or_update_msg_to_conv(**self.model_dump())


class ContextMessage(BaseModel):
    """Context message class. This class is used to create the context message for the reasoning context."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_default=True,
        use_enum_values=True,
    )

    content: Optional[Union[List[dict], str]] = None
    tool_calls: Optional[List[dict]] = None
    tool_call_id: Optional[str] = None
    role: RoleTypes = RoleTypes.system

    def to_llm_msg(self):
        """Convert the context message to the llm message."""
        msg = {
            "role": self.role,
            "content": self.content,
        }
        if self.role == RoleTypes.system:
            return msg

        if self.role == RoleTypes.user:
            return format_user_message(msg)

        if self.role == RoleTypes.assistant:
            if self.tool_calls:
                msg["tool_calls"] = self.tool_calls
            if not self.content:
                msg["content"] = []
            return msg

        if self.role == RoleTypes.tool:
            msg["tool_call_id"] = self.tool_call_id
            return msg

    @classmethod
    def from_json(cls, json_data):
        """Create the context message from the json data."""
        return cls(**json_data)
