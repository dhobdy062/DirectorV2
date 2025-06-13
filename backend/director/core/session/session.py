"""
Session management class
"""

from typing import Union
from flask_socketio import emit

from director.db.base import BaseDB
from .enums import MsgType
from .messages import InputMessage, OutputMessage, ContextMessage
from .events import BaseEvent


class Session:
    """A class to manage and interact with a session in the database. The session is used to store the conversation and reasoning context messages."""

    def __init__(
        self,
        db: BaseDB,
        session_id: str = "",
        conv_id: str = "",
        collection_id: str = None,
        video_id: str = None,
        **kwargs,
    ):
        self.db = db
        self.session_id = session_id
        self.conv_id = conv_id
        self.conversations = []
        self.video_id = video_id
        self.collection_id = collection_id
        self.reasoning_context = []
        self.state = {}
        self.output_message = OutputMessage(
            db=self.db, session_id=self.session_id, conv_id=self.conv_id
        )

        self.get_context_messages()

    def save_context_messages(self):
        """Save the reasoning context messages to the database."""
        context = {
            "reasoning": [message.to_llm_msg() for message in self.reasoning_context],
        }
        self.db.add_or_update_context_msg(self.session_id, context)

    def get_context_messages(self):
        """Get the reasoning context messages from the database."""
        if not self.reasoning_context:
            context = self.db.get_context_messages(self.session_id)
            self.reasoning_context = [
                ContextMessage.from_json(message)
                for message in context.get("reasoning", [])
            ]

        return self.reasoning_context

    def create(self):
        """Create a new session in the database."""
        self.db.create_session(**self.__dict__)

    def new_message(
        self, msg_type: MsgType = MsgType.output, **kwargs
    ) -> Union[InputMessage, OutputMessage]:
        """Returns a new input/output message object.

        :param MsgType msg_type: The type of the message, input or output.
        :param dict kwargs: The message attributes.
        :return: The input/output message object.
        """
        if msg_type == MsgType.input:
            return InputMessage(
                db=self.db,
                session_id=self.session_id,
                conv_id=self.conv_id,
                **kwargs,
            )
        return OutputMessage(
            db=self.db,
            session_id=self.session_id,
            conv_id=self.conv_id,
            **kwargs,
        )

    def get(self):
        """Get the session from the database."""
        session = self.db.get_session(self.session_id)
        conversation = self.db.get_conversations(self.session_id)
        session["conversation"] = conversation
        return session

    def get_all(self):
        """Get all the sessions from the database."""
        return self.db.get_sessions()

    def delete(self):
        """Delete the session from the database."""
        return self.db.delete_session(self.session_id)

    def emit_event(self, event: BaseEvent, namespace="/chat"):
        """Emits a structured WebSocket event to notify all clients about updates."""
        event_payload = event.model_dump()

        try:
            emit("event", event_payload, namespace=namespace)
        except Exception:
            pass
