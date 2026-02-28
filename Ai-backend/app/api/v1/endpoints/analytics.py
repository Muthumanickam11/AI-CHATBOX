from fastapi import APIRouter
from app.schemas.analytics import AnalyticsLog
from datetime import datetime

router = APIRouter()

@router.get("/analytics/{user_id}", response_model=AnalyticsLog)
async def get_analytics(user_id: str, conversation_id: str):
    """
    Day 7: Analytics endpoint
    Returns analytics data for a specific conversation
    """
    # In production, this would query from database
    # For now, return mock data matching the blueprint
    return AnalyticsLog(
        user_id=user_id,
        conversation_id=conversation_id,
        tokens_used=1024,
        latency="2.3s",
        model="gpt-4",
        timestamp=datetime.utcnow().isoformat()
    )
