from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatMessageCreate(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    id: int
    message: str
    sender: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    is_active: bool
    message_count: int
    
    class Config:
        from_attributes = True
