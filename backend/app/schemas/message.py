from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    session_id: int

class MessageUpdate(MessageBase):
    pass

class MessageInDBBase(MessageBase):
    id: int
    session_id: int
    tokens: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True

class Message(MessageInDBBase):
    pass