from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Day 8: Deployment + Monitoring (Health Check).
    """
    return {
        "status": "healthy",
        "uptime": "99.97%", # Static for demo
        "requests_today": 1280,
        "average_latency": "1.9s",
        "error_rate": "0.4%",
        "timestamp": datetime.utcnow()
    }
