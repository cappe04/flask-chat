from datetime import datetime

from pydantic import BaseModel, field_validator, ValidationError

MAX_MESSAGE_LENGTH = 256 # maybe in .env

class DatabaseMessage(BaseModel):
    channel_id: int
    user_id: int
    message: str
    timestamp: int

    @field_validator("message")
    @classmethod
    def cap_message_length(cls, v: str):
        if len(v) > MAX_MESSAGE_LENGTH:
            return v[:MAX_MESSAGE_LENGTH]
        return v

class ChatMessage(DatabaseMessage):
    username: str
    message_id: int
    timestamp: str | int

    @field_validator("timestamp")
    @classmethod
    def convert_timestamp(cls, v: int) -> str:
        return datetime.fromtimestamp(v).strftime('%Y-%m-%d %H:%M:%S')

