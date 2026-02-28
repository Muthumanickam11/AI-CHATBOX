"""Hybrid Chat Endpoint - JSON First, AI Fallback"""
from fastapi import APIRouter, HTTPException
from app.schemas.hybrid_chat import HybridChatRequest, HybridChatResponse
from app.services.json_logic import get_knowledge_base
from app.services.ai_logic import generate_ai_response
from app.services.db_logic import get_supabase
from datetime import datetime

router = APIRouter()

@router.post("/chat", response_model=HybridChatResponse)
async def hybrid_chat(request: HybridChatRequest):
    """
    Hybrid Response Engine:
    1. Check JSON knowledge base
    2. If no match, call OpenAI
    3. Save to Supabase
    """
    
    # Step 1: Normalize prompt
    normalized_prompt = request.prompt.lower().strip()
    
    # Step 2: Try JSON match first
    kb = get_knowledge_base()
    json_match = kb.find_best_match(normalized_prompt)
    
    if json_match:
        # JSON match found - return immediately
        reply = json_match["answer"]
        source = "json_match"
        tokens_used = 0
        processing_time = "0.01s"
    else:
        # Step 3: Fallback to AI
        ai_result = await generate_ai_response(
            prompt=request.prompt,
            mode=request.mode
        )
        reply = ai_result["reply"]
        source = "ai_generated"
        tokens_used = ai_result["tokens_used"]
        processing_time = ai_result["processing_time"]
    
    # Step 4: Save to Supabase
    db = get_supabase()
    await db.insert_chat_log(
        user_id=request.user_id,
        session_id=request.session_id,
        prompt=request.prompt,
        response=reply,
        source=source,
        metadata={"mode": request.mode, "tokens": tokens_used}
    )
    
    return HybridChatResponse(
        reply=reply,
        source=source,
        session_id=request.session_id,
        tokens_used=tokens_used,
        processing_time=processing_time,
        timestamp=datetime.utcnow()
    )

@router.get("/history/{user_id}")
async def get_history(user_id: str, limit: int = 10):
    """Retrieve chat history for a user"""
    db = get_supabase()
    history = await db.fetch_history(user_id, limit)
    return {"user_id": user_id, "history": history, "count": len(history)}

@router.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "AI Knowledge Chat Backend"}
