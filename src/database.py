from typing import Any, Iterator
from .schemas import DatabaseMessage, ChatMessage

MOCK_DATABASE = {
    "users": [
        {
            "user_id": 0, 
            "username": "Casper Bené", 
            "password": "abc123"
        },
        {
            "user_id": 1, 
            "username": "Donald Trump", 
            "password": "MAGA2024" 
        },
        {
            "user_id": 2,
            "username": "Sleepy Joe", 
            "password": "Uh..." 
        },
        {
            "user_id": 3, 
            "username": "Barack Obama", 
            "password": "AGM-120 Maverick" 
        },
        {
            "user_id": 4, 
            "username": "Guest", 
            "password": "bajs123" 
        },
    ],
    "channels": [
        {
            "channel_id": 0,
            "channel_name": "All"
        },
        {
            "channel_id": 3,
            "channel_name": "Oval Office"
        },
    ],
    "messages": [
        # {
        #     "message_id": 0,
        #     "channel_id": 0,
        #     "user_id": 0,
        #     "message": "",
        #     "timestamp": 0
        # }
    ],
}

def append_message(message: DatabaseMessage) -> int:
    message_id = len(MOCK_DATABASE["messages"])
    MOCK_DATABASE["messages"].append(message.model_dump() | { "message_id": message_id })
    return message_id

def get_messages(identifier: str, match: Any, count: int) -> Iterator[ChatMessage]:
    for i, message in enumerate(MOCK_DATABASE["messages"]):
        if i > count: 
            break
        if message[identifier] == match:
            yield ChatMessage(**message, username=get_username(message["user_id"]))


def get_login(username: str, password: str) -> int | None:
    for user in MOCK_DATABASE["users"]:
        if user["username"] == username and user["password"] == password:
            return user["user_id"]     
    return

def __get_query(table: str, query: str, identifier: str, match: Any) -> Any | None:
    # FROM "table" SELECT "query" WHERE "identifier" = "match"
    for column in MOCK_DATABASE[table]:
        if column[identifier] == match:
            return column[query]
    return

def get_username(user_id: int | Any) -> str | None:
    return __get_query("users", "username", "user_id", user_id)

def get_channel_name(user_id: int | Any) -> str | None:
    return __get_query("channels", "channel_name", "channel_id", user_id)

def get_channels():
    for channel in MOCK_DATABASE["channels"]:
        yield (channel["channel_id"], channel["channel_name"])


def __validate_query(table: str, query: str, match: Any) -> bool:
    for column in MOCK_DATABASE[table]:
        if column[query] == match:
            return True
    return False

def validate_channel(channel_id: int | Any) -> bool:
    return __validate_query("channels", "channel_id", channel_id)

def validate_user(user_id: int | Any) -> bool:
    return __validate_query("users", "user_id", user_id)
