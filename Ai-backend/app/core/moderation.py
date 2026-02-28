from app.core.config import get_settings

def check_safety(prompt: str):
    # Day 7: Moderation
    unsafe_keywords = ["hack", "violence", "hate"]
    for word in unsafe_keywords:
        if word in prompt.lower():
            return {
                "flagged": True,
                "reason": "unsafe_content" # Matching prompt example
            }
    return {"flagged": False}
