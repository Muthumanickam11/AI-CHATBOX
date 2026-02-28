"""Hybrid Chat Schemas"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HybridChatRequest(BaseModel):
    user_id: str
    session_id: str
    prompt: str
    mode: str = "balanced"  # creative, balanced, precise

class HybridChatResponse(BaseModel):
    reply: str
    source: str  # "json_match" or "ai_generated"
    session_id: str
    tokens_used: int = 0
    processing_time: str
    timestamp: datetime
