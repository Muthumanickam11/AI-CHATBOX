# 🏗️ Hybrid Backend Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│                    http://localhost:3000                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP POST /api/v1/hybrid/chat
                             │ {user_id, session_id, prompt, mode}
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND (main.py)                     │
│                    http://localhost:8004                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              CORS Middleware (Security)                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Router: /api/v1/hybrid/chat                    │   │
│  │           (hybrid_chat.py endpoint)                      │   │
│  └────────────────────┬─────────────────────────────────────┘   │
└─────────────────────────┼─────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │   HYBRID DECISION ENGINE            │
        │   (Step 1: Normalize Prompt)        │
        └─────────────────┬───────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │   JSON KNOWLEDGE BASE SEARCH        │
        │   (services/json_logic.py)          │
        │                                     │
        │   • Load data/knowledge_base.json   │
        │   • Exact match check               │
        │   • Partial match check             │
        └─────────────────┬───────────────────┘
                          │
                ┌─────────┴─────────┐
                │                   │
             MATCH               NO MATCH
                │                   │
                ▼                   ▼
    ┌───────────────────┐   ┌──────────────────────┐
    │  RETURN JSON      │   │   OPENAI API CALL    │
    │  ANSWER           │   │  (services/ai_logic) │
    │                   │   │                      │
    │  source: "json"   │   │  Mode-based config:  │
    │  tokens: 0        │   │  • Creative: 0.9     │
    │  time: ~0.01s     │   │  • Balanced: 0.7     │
    │                   │   │  • Precise: 0.3      │
    │                   │   │                      │
    │                   │   │  source: "ai"        │
    │                   │   │  tokens: 50-300      │
    │                   │   │  time: ~1-3s         │
    └─────────┬─────────┘   └──────────┬───────────┘
              │                        │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   SUPABASE STORAGE     │
              │  (services/db_logic)   │
              │                        │
              │  • Save chat log       │
              │  • Store metadata      │
              │  • Track source        │
              └────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   RESPONSE TO CLIENT   │
              │                        │
              │  {                     │
              │    reply: "...",       │
              │    source: "json/ai",  │
              │    tokens_used: N,     │
              │    processing_time     │
              │  }                     │
              └────────────────────────┘
```

## Service Layer Architecture

```
app/services/
├── json_logic.py
│   ├── JSONKnowledgeBase (Class)
│   │   ├── __init__()
│   │   ├── load_knowledge_base()
│   │   └── find_best_match(query)
│   └── get_knowledge_base() [Singleton]
│
├── ai_logic.py
│   ├── MODE_CONFIGS (Dict)
│   │   ├── creative: {temp: 0.9, tokens: 300}
│   │   ├── balanced: {temp: 0.7, tokens: 250}
│   │   └── precise: {temp: 0.3, tokens: 200}
│   └── generate_ai_response(prompt, mode, history)
│
└── db_logic.py
    ├── SupabaseService (Class)
    │   ├── __init__()
    │   ├── initialize()
    │   ├── insert_chat_log(...)
    │   └── fetch_history(user_id)
    └── get_supabase() [Singleton]
```

## Data Flow Diagram

```
┌──────────┐
│  User    │
│  Input   │
└────┬─────┘
     │
     │ "What is AI?"
     ▼
┌─────────────────┐
│  Normalization  │
│  "what is ai?"  │
└────┬────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  knowledge_base.json                │
│  [                                  │
│    {                                │
│      "question": "What is AI?",     │
│      "answer": "AI is..."           │
│    },                               │
│    ...                              │
│  ]                                  │
└────┬────────────────────────────────┘
     │
     │ Match found!
     ▼
┌─────────────────┐
│  Return Answer  │
│  (0 API calls)  │
│  (0 tokens)     │
│  (0 cost)       │
└─────────────────┘

OR (if no match)

     │
     │ No match
     ▼
┌─────────────────────────────────────┐
│  OpenAI GPT-3.5-turbo               │
│  POST https://api.openai.com/...    │
│                                     │
│  Request:                           │
│  {                                  │
│    model: "gpt-3.5-turbo",          │
│    messages: [...],                 │
│    temperature: 0.7,                │
│    max_tokens: 250                  │
│  }                                  │
└────┬────────────────────────────────┘
     │
     │ Response
     ▼
┌─────────────────┐
│  AI Generated   │
│  Answer         │
│  (~200 tokens)  │
│  (~$0.0004)     │
└─────────────────┘
```

## Cost Optimization Strategy

```
100 Requests Scenario:

WITHOUT Hybrid (Pure AI):
├── 100 requests × 200 tokens avg
├── 20,000 total tokens
└── Cost: ~$0.04

WITH Hybrid (70% JSON hit rate):
├── 70 requests from JSON (0 tokens)
├── 30 requests from AI (6,000 tokens)
└── Cost: ~$0.012

💰 SAVINGS: 70% cost reduction
⚡ SPEED: 70% faster responses
```

## Security Layers

```
┌─────────────────────────────────────┐
│  1. CORS Middleware                 │
│     • Allowed origins only          │
│     • Credentials handling          │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  2. Pydantic Validation             │
│     • Type checking                 │
│     • Required fields               │
│     • Data sanitization             │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  3. Environment Variables           │
│     • API keys in .env              │
│     • Never in code                 │
│     • .gitignore protection         │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  4. Error Handling                  │
│     • Try/except blocks             │
│     • Friendly error messages       │
│     • No sensitive data exposure    │
└─────────────────────────────────────┘
```

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    PRODUCTION                            │
│                                                          │
│  ┌────────────────┐         ┌──────────────────┐        │
│  │   Frontend     │         │    Backend       │        │
│  │   (Vercel)     │◄────────┤   (Render/       │        │
│  │                │  HTTPS  │    Railway)      │        │
│  └────────────────┘         └─────────┬────────┘        │
│                                       │                 │
│                             ┌─────────┴─────────┐       │
│                             │                   │       │
│                    ┌────────▼────────┐  ┌───────▼──────┐│
│                    │   Supabase      │  │   OpenAI     ││
│                    │   (Database)    │  │   (LLM API)  ││
│                    └─────────────────┘  └──────────────┘│
└──────────────────────────────────────────────────────────┘
```

## File Structure

```
Ai-backend/
│
├── app/
│   ├── main.py                      # FastAPI app entry
│   ├── services/                    # Business logic
│   │   ├── __init__.py
│   │   ├── json_logic.py           # JSON KB search
│   │   ├── ai_logic.py             # OpenAI integration
│   │   └── db_logic.py             # Supabase client
│   ├── api/v1/endpoints/
│   │   ├── hybrid_chat.py          # Hybrid endpoint
│   │   ├── chat.py                 # Original chat
│   │   ├── history.py
│   │   ├── auth.py
│   │   └── ...
│   ├── schemas/
│   │   ├── hybrid_chat.py          # Pydantic models
│   │   └── ...
│   ├── models/                      # SQLAlchemy models
│   ├── core/                        # Config, security
│   └── db/                          # Database session
│
├── data/
│   └── knowledge_base.json          # Local Q&A cache
│
├── tests/
│   ├── test_hybrid.py              # Hybrid tests
│   └── ...
│
├── .env                             # Secrets (gitignored)
├── .env.example                     # Template
├── .gitignore
├── requirements.txt
├── README.md
├── IMPLEMENTATION_STATUS.md
└── ARCHITECTURE.md                  # This file
```

---

**Built with**: FastAPI, Supabase, OpenAI GPT-3.5-turbo  
**Architecture Pattern**: Service-Oriented, Hybrid Caching  
**Optimization**: Cost-efficient, Speed-optimized
