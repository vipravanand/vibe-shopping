from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    message: str
    session_id: str

    class Config:
        extra = "forbid"
        schema_extra = {
            "examples": [
                {
                    "message": "Hello, how are you?",
                    "user_id": "123"
                }
            ]
        }