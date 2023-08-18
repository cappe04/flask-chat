from pydantic import BaseModel, FieldValidationInfo, field_validator, ValidationError

MAX_MESSAGE_LENGTH = 256 # maybe in .env

class ChatMessage(BaseModel):
    user_id: str # should be int later when actual user_id
    channel_id: int
    message: str
    timestamp: int

    @field_validator("message")
    @classmethod
    def cap_message_length(cls, v: str, info: FieldValidationInfo) -> str:
        if len(v) > MAX_MESSAGE_LENGTH:
            return v[:MAX_MESSAGE_LENGTH]
        return v