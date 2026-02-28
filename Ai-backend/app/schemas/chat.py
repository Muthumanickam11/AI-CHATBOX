from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    conversation_id: Optional[str] = None
    prompt: Optional[str] = None
    query: Optional[str] = None # Day 5 alias for prompt
    user: Optional[dict] = None # For Day 2 input support
    action: Optional[str] = None # For Day 3 support logic
    limit: Optional[int] = None # For Day 3 support logic
    settings: Optional[dict] = None # For future use

class ChatResponse(BaseModel):
    reply: Optional[str] = None
    answer: Optional[str] = None # Day 5/6 alias
    model: Optional[str] = None
    timestamp: Optional[datetime] = None
    session_id: Optional[str] = None
    conversation_id: Optional[str] = None
    stored: Optional[bool] = None
    tokens_used: Optional[int] = None
    processing_time: Optional[str] = None
    sources: Optional[list] = None # Day 6 RAG
    # Day 7 Moderation fields
    user_id: Optional[str] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    message: Optional[str] = None
