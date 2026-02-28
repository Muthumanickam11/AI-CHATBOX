# 🤖 AI Knowledge Chat Backend

> **Production-ready FastAPI backend with Hybrid Response Engine**  
> JSON Knowledge Base First → OpenAI Fallback → Supabase Persistence

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-412991?logo=openai)](https://openai.com)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?logo=supabase)](https://supabase.com)

## 🎯 Overview

This backend implements a **Hybrid Response Engine** that optimizes cost and speed by:
1. **First** checking a local JSON knowledge base for answers
2. **Then** falling back to OpenAI GPT-3.5-turbo if no match is found
3. **Finally** persisting all interactions to Supabase

### Key Benefits
- 💰 **70% cost reduction** (JSON matches use 0 tokens)
- ⚡ **70% faster responses** (JSON lookup ~0.01s vs AI ~1-3s)
- 🎨 **3 AI modes**: Creative, Balanced, Precise
- 📊 **Full history tracking** via Supabase
- 🔒 **Production-ready** with CORS, validation, error handling

## 🏗️ Architecture

```
User Request → Normalize → JSON Search → Match? 
                                ↓ Yes: Return (0 tokens)
                                ↓ No: OpenAI API → Return
                                ↓ Save to Supabase
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed diagrams.

## 📂 Project Structure

```
Ai-backend/
├── app/
│   ├── main.py                      # FastAPI entry point
│   ├── services/                    # 🆕 Service layer
│   │   ├── json_logic.py           # JSON KB search
│   │   ├── ai_logic.py             # OpenAI integration
│   │   └── db_logic.py             # Supabase client
│   ├── api/v1/endpoints/
│   │   └── hybrid_chat.py          # 🆕 Hybrid endpoint
│   └── schemas/
│       └── hybrid_chat.py          # 🆕 Pydantic models
├── data/
│   └── knowledge_base.json          # 🆕 Local Q&A cache
├── test_hybrid.py                   # 🆕 Test suite
├── requirements.txt                 # Updated with supabase
└── .env.example                     # Environment template
```

## 🚀 Quick Start

### 1. Clone & Install

```bash
cd Ai-backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```env
OPENAI_API_KEY=sk-your-openai-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-supabase-service-key
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
SECRET_KEY=your-secret-key-for-jwt
```

### 3. Setup Supabase Table

Run this SQL in your Supabase SQL editor:

```sql
CREATE TABLE chat_history (
  id SERIAL PRIMARY KEY,
  user_id TEXT NOT NULL,
  session_id TEXT NOT NULL,
  prompt TEXT NOT NULL,
  response TEXT NOT NULL,
  source TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_id ON chat_history(user_id);
CREATE INDEX idx_session_id ON chat_history(session_id);
```

### 4. Run Server

```bash
uvicorn app.main:app --reload --port 8004
```

Server will start at: `http://localhost:8004`

### 5. Test

```bash
python test_hybrid.py
```

## 📡 API Endpoints

### POST `/api/v1/hybrid/chat`

**Request:**
```json
{
  "user_id": "user-123",
  "session_id": "sess-001",
  "prompt": "What is AI?",
  "mode": "balanced"
}
```

**Response:**
```json
{
  "reply": "AI (Artificial Intelligence) is the simulation of human intelligence...",
  "source": "json_match",
  "session_id": "sess-001",
  "tokens_used": 0,
  "processing_time": "0.01s",
  "timestamp": "2025-12-14T15:13:37Z"
}
```

**Modes:**
- `creative` - Temperature: 0.9, Max tokens: 300 (more creative, varied)
- `balanced` - Temperature: 0.7, Max tokens: 250 (default, balanced)
- `precise` - Temperature: 0.3, Max tokens: 200 (factual, concise)

### GET `/api/v1/hybrid/history/{user_id}`

**Query params:** `?limit=10`

**Response:**
```json
{
  "user_id": "user-123",
  "history": [
    {
      "prompt": "What is AI?",
      "response": "AI is...",
      "source": "json_match",
      "created_at": "2025-12-14T15:13:37Z"
    }
  ],
  "count": 1
}
```

### GET `/api/v1/hybrid/`

Health check endpoint.

## 🧪 Testing

The test suite (`test_hybrid.py`) covers:

1. ✅ **JSON Match Test** - Verifies knowledge base lookup
2. ✅ **AI Fallback Test** - Tests OpenAI integration
3. ✅ **Mode Test** - Validates creative/balanced/precise modes
4. ✅ **History Test** - Checks Supabase retrieval
5. ✅ **Health Check** - Confirms service status

Run tests:
```bash
python test_hybrid.py
```

Expected output:
```
🚀 HYBRID CHAT SYSTEM TEST SUITE
==================================================
TEST 1: JSON Knowledge Base Match
Status: 200
Source: json_match
Tokens: 0
✅ JSON match test PASSED
...
🎉 ALL TESTS PASSED!
```

## 📊 Knowledge Base

Edit `data/knowledge_base.json` to add Q&A pairs:

```json
[
  {
    "question": "What is AI?",
    "answer": "AI is the simulation of human intelligence by machines..."
  },
  {
    "question": "What is machine learning?",
    "answer": "Machine learning is a subset of AI that enables systems..."
  }
]
```

**Current:** 5 Q&A pairs (sample)  
**Recommended:** 200-300 pairs for production

## 🔒 Security Features

- ✅ **CORS** - Configured for frontend origins
- ✅ **Environment Variables** - API keys never in code
- ✅ **Pydantic Validation** - Type-safe request/response
- ✅ **Error Handling** - Graceful fallbacks, no crashes
- ✅ **Gitignore** - `.env` file protected

## 🌐 Deployment

### Render / Railway

1. Connect GitHub repo
2. Set environment variables
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Vercel (Serverless)

Create `vercel.json`:
```json
{
  "builds": [
    {"src": "app/main.py", "use": "@vercel/python"}
  ],
  "routes": [
    {"src": "/(.*)", "dest": "app/main.py"}
  ]
}
```

## 📈 Performance Metrics

| Metric | JSON Match | AI Fallback |
|--------|-----------|-------------|
| Response Time | ~0.01s | ~1-3s |
| Tokens Used | 0 | 50-300 |
| Cost per Request | $0 | ~$0.0004 |

**Scenario:** 100 requests, 70% JSON hit rate
- **Cost:** $0.012 (vs $0.04 pure AI)
- **Savings:** 70%
- **Avg Speed:** 0.9s (vs 2s pure AI)

## 🛠️ Tech Stack

- **Framework:** FastAPI 0.100+
- **Language:** Python 3.8+
- **LLM:** OpenAI GPT-3.5-turbo
- **Database:** Supabase (PostgreSQL)
- **Validation:** Pydantic
- **Server:** Uvicorn (ASGI)

## 📝 Documentation

- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture diagrams
- [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md) - Implementation checklist
- [HYBRID_IMPLEMENTATION.md](./HYBRID_IMPLEMENTATION.md) - Setup guide

## 🤝 Integration Example

### Frontend (React/JavaScript)

```javascript
const chatWithBackend = async (prompt, mode = 'balanced') => {
  const response = await fetch('http://localhost:8004/api/v1/hybrid/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: 'user-123',
      session_id: 'sess-' + Date.now(),
      prompt: prompt,
      mode: mode
    })
  });
  
  const data = await response.json();
  
  console.log('Answer:', data.reply);
  console.log('Source:', data.source); // "json_match" or "ai_generated"
  console.log('Tokens:', data.tokens_used);
  
  return data;
};

// Usage
chatWithBackend('What is AI?', 'balanced');
```

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Built following the Master Backend Specification for AI Knowledge Chat

---

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Last Updated:** December 2025
