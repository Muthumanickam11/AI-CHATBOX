import openai
from app.core.config import get_settings
from datetime import datetime
import time

settings = get_settings()

async def generate_reply(prompt: str, model: str = "gpt-4", settings_dict: dict = None):
    # Day 5 Logic
    if not settings_dict:
        settings_dict = {}
        
    temperature = settings_dict.get("temperature", 0.7)
    max_tokens = settings_dict.get("max_tokens", 250)
    
    start_time = time.time()
    
    if settings.OPENAI_API_KEY:
        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            reply = response.choices[0].message.content
            tokens = response.usage.total_tokens
        except Exception as e:
            reply = f"AI Error: {str(e)}"
            tokens = 0
    else:
        # Simulation
        reply = "Renewable energy reduces pollution and supports sustainable power generation." # Day 5 example
        tokens = 168
        
    duration = time.time() - start_time
    
    return {
        "reply": reply,
        "tokens_used": tokens,
        "processing_time": f"{duration:.1f}s"
    }
