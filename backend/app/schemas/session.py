from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionBase(BaseModel):
    title: str

class SessionCreate(SessionBase):
    user_id: int

class SessionUpdate(SessionBase):
    pass

class SessionInDBBase(SessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Session(SessionInDBBase):
    pass