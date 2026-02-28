from datetime import datetime
from typing import Optional

class AnalyticsTracker:
    """Day 7: Analytics tracking for monitoring usage"""
    
    @staticmethod
    def log_request(user_id: str, conversation_id: str, tokens_used: int, 
                   latency: float, model: str):
        """
        Log analytics data for a request.
        In production, this would write to a database or analytics service.
        """
        analytics_data = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "tokens_used": tokens_used,
            "latency": f"{latency:.1f}s",
            "model": model,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # In production: write to database or send to analytics service
        # For now, we'll just print for demonstration
        print(f"[ANALYTICS] {analytics_data}")
        
        return analytics_data
