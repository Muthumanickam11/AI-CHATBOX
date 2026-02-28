from pydantic import BaseModel
from typing import List, Optional

class HistoryRequest(BaseModel):
    user_id: str # Accepting string to match "user-001" format or int
    action: str = "get_history"
    limit: Optional[int] = 10

class HistoryItem(BaseModel):
    prompt: str
    reply: str

class HistoryResponse(BaseModel):
    history: List[HistoryItem]
    count: int
