from pydantic import BaseModel, FieldValidationInfo, field_validator, ValidationError

MAX_MESSAGE_LENGTH = 256 # maybe in .env

class ChatMessage(BaseModel):
    username: str
    channel_id: int
    message: str
    timestamp: int
    message_id: int

    @field_validator("username", "message") # not really needed for username but why not...
    @classmethod
    def cap_string_length(cls, v: str) -> str:
        if len(v) > MAX_MESSAGE_LENGTH:
            return v[:MAX_MESSAGE_LENGTH]
        return v


class DatabaseMessage(BaseModel):
    channel_id: int
    user_id: int
    message: str
    timestamp: int

    @field_validator("message")
    @classmethod
    def cap_string_length(cls, v: str):
        if len(v) > MAX_MESSAGE_LENGTH:
            return v[:MAX_MESSAGE_LENGTH]
        return v