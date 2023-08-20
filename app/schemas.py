from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, ValidationError

from .settings import MESSAGE_MAX_LENGTH 

class DbUser(BaseModel):
    username: str = Field(..., max_length=30)
    password: str = Field(..., max_length=60)
    profile_picture: Optional[bytes] = None

class DbMessage(BaseModel):
    channel_id: int
    user_id: int
    message: str = Field(..., max_length=MESSAGE_MAX_LENGTH)
    post_time: int

def convert_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

