"""Database Service - Supabase integration for chat history"""
import os
from typing import List, Dict, Optional
from datetime import datetime
from supabase import create_client, Client

class SupabaseService:
    def __init__(self):
        self.client: Optional[Client] = None
        self.initialize()
    
    def initialize(self):
        """Initialize Supabase client"""
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if url and key:
            try:
                self.client = create_client(url, key)
                print("✓ Supabase connected")
            except Exception as e:
                print(f"⚠ Supabase connection failed: {e}")
        else:
            print("⚠ Supabase credentials not configured")
    
    async def insert_chat_log(
        self,
        user_id: str,
        session_id: str,
        prompt: str,
        response: str,
        source: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Save chat interaction to Supabase"""
        if not self.client:
            return False
        
        try:
            data = {
                "user_id": user_id,
                "session_id": session_id,
                "prompt": prompt,
                "response": response,
                "source": source,
                "metadata": metadata or {},
                "created_at": datetime.utcnow().isoformat()
            }
            self.client.table("chat_history").insert(data).execute()
            return True
        except Exception as e:
            print(f"Error saving to Supabase: {e}")
            return False
    
    async def fetch_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve chat history for a user"""
        if not self.client:
            return []
        
        try:
            response = self.client.table("chat_history")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error fetching history: {e}")
            return []

# Singleton instance
_supabase_instance = None

def get_supabase() -> SupabaseService:
    """Get singleton Supabase instance"""
    global _supabase_instance
    if _supabase_instance is None:
        _supabase_instance = SupabaseService()
    return _supabase_instance
