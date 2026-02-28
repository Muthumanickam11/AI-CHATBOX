"""AI Service - OpenAI integration with mode-based configuration"""
import openai
import time
from typing import Dict, Optional
from app.core.config import get_settings

settings = get_settings()

MODE_CONFIGS = {
    "creative": {"temperature": 0.9, "max_tokens": 300},
    "balanced": {"temperature": 0.7, "max_tokens": 250},
    "precise": {"temperature": 0.3, "max_tokens": 200}
}

async def generate_ai_response(
    prompt: str, 
    mode: str = "balanced",
    history: Optional[list] = None
) -> Dict:
    """Generate AI response with mode-based settings"""
    start_time = time.time()
    
    # Get mode configuration
    config = MODE_CONFIGS.get(mode, MODE_CONFIGS["balanced"])
    
    # Build messages with history
    messages = []
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})
    
    try:
        if settings.OPENAI_API_KEY:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=config["temperature"],
                max_tokens=config["max_tokens"]
            )
            reply = response.choices[0].message.content
            tokens = response.usage.total_tokens
        else:
            # Fallback when no API key
            reply = "I'm having trouble thinking right now. Please check API configuration."
            tokens = 0
    except Exception as e:
        print(f"OpenAI Error: {e}")
        reply = "I'm having trouble thinking right now. Please try again later."
        tokens = 0
    
    duration = time.time() - start_time
    
    return {
        "reply": reply,
        "tokens_used": tokens,
        "processing_time": f"{duration:.2f}s",
        "mode": mode
    }
