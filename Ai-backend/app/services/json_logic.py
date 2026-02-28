"""JSON Knowledge Base Service - Handles local Q&A matching"""
import json
import os
from typing import Optional, Dict
from pathlib import Path

class JSONKnowledgeBase:
    def __init__(self):
        self.knowledge_base = []
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load knowledge base from JSON file"""
        try:
            kb_path = Path(__file__).parent.parent.parent / "data" / "knowledge_base.json"
            if kb_path.exists():
                with open(kb_path, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
                print(f"✓ Loaded {len(self.knowledge_base)} Q&A pairs")
            else:
                print(f"⚠ Knowledge base not found at {kb_path}")
                self.knowledge_base = []
        except Exception as e:
            print(f"⚠ Error loading knowledge base: {e}")
            self.knowledge_base = []
    
    def find_best_match(self, query: str) -> Optional[Dict[str, str]]:
        """Search for matching question in knowledge base"""
        if not query or not self.knowledge_base:
            return None
        
        # Normalize query
        normalized_query = query.lower().strip()
        
        # Exact match
        for item in self.knowledge_base:
            if item["question"].lower().strip() == normalized_query:
                return {"answer": item["answer"], "match_type": "exact"}
        
        # Partial match (containment)
        for item in self.knowledge_base:
            question_lower = item["question"].lower()
            if normalized_query in question_lower or question_lower in normalized_query:
                return {"answer": item["answer"], "match_type": "partial"}
        
        return None

# Singleton instance
_kb_instance = None

def get_knowledge_base() -> JSONKnowledgeBase:
    """Get singleton knowledge base instance"""
    global _kb_instance
    if _kb_instance is None:
        _kb_instance = JSONKnowledgeBase()
    return _kb_instance
