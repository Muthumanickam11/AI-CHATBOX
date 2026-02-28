from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chat import ChatRequest, ChatResponse
from app.db.session import get_db
from app.models.user import User
from app.models.chat import Chat
from datetime import datetime
from app.core.config import get_settings
from app.core import ai
from app.core import moderation
from app.core import rag
from app.core.analytics import AnalyticsTracker
import uuid
import time

router = APIRouter()
settings = get_settings()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Unified Chat Endpoint (Days 1-7).
    """
    start_time = time.time()
    
    # Normalize prompt/query
    user_prompt = request.prompt or request.query
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Prompt or query required")

    # 1. Moderation (Day 7)
    mod_result = moderation.check_safety(user_prompt)
    if mod_result["flagged"]:
        return ChatResponse(
            user_id="user-001",
            message=user_prompt,
            status="blocked",
            reason=mod_result["reason"]
        )

    # 2. User Management (Day 2)
    user_obj = None
    if request.user:
        result = await db.execute(select(User).filter(User.email == request.user['email']))
        user_obj = result.scalars().first()
        if not user_obj:
            user_obj = User(email=request.user['email'], name=request.user.get('name'))
            db.add(user_obj)
            await db.commit()
            await db.refresh(user_obj)
    
    # 3. RAG / Context (Day 6)
    # Mock retrieval logic based on Day 6 requirement
    sources = []
    augmented_prompt = user_prompt
    
    # Check if we should use RAG (Simple heuristic: if "document" in prompt or implicit)
    # For Blueprint demo, we assume RAG is active or check if documents exist.
    # We'll augment the prompt if "uploaded document" is mentioned for demo purposes
    if "document" in user_prompt.lower() or "uploaded" in user_prompt.lower():
         # Mocking retrieved chunk
         sources = [{ "doc_id": "doc-201", "page": 4, "relevance": 0.91 }]
         augmented_prompt = f"Context: AI systems learn from data.\n\nQuery: {user_prompt}"

    # 4. AI Logic (Day 5)
    ai_result = await ai.generate_reply(
        prompt=augmented_prompt, 
        settings_dict=request.settings
    )
    
    reply_text = ai_result["reply"]
    tokens = ai_result["tokens_used"]
    proc_time = ai_result["processing_time"]

    # 5. Conversation Management
    conv_id = request.conversation_id or f"conv-{uuid.uuid4().hex[:6]}"
    
    # 6. Store Chat (Day 2)
    stored = False
    if user_obj:
        chat_entry = Chat(
            conversation_id=conv_id,
            user_id=user_obj.id,
            prompt=user_prompt,
            reply=reply_text
        )
        db.add(chat_entry)
        await db.commit()
        stored = True

    # 7. Analytics Logging (Day 7)
    request_latency = time.time() - start_time
    if user_obj:
        AnalyticsTracker.log_request(
            user_id=str(user_obj.id),
            conversation_id=conv_id,
            tokens_used=tokens,
            latency=request_latency,
            model="gpt-4"
        )

    return ChatResponse(
        reply=reply_text,
        answer=reply_text, # providing both
        model="gpt-4",
        timestamp=datetime.utcnow(),
        session_id=request.session_id,
        conversation_id=conv_id,
        stored=stored,
        tokens_used=tokens,
        processing_time=proc_time,
        sources=sources if sources else None
    )
