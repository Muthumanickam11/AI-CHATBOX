from pydantic import BaseModel
from typing import Optional

class AnalyticsLog(BaseModel):
    user_id: str
    conversation_id: str
    tokens_used: int
    latency: str
    model: str
    timestamp: Optional[str] = None
