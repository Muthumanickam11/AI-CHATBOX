# 🚀 QUICK START GUIDE - Hybrid Backend

## ⚡ 5-Minute Setup

### Step 1: Verify Installation ✅
```bash
# You should already have these installed
pip install -r requirements.txt
```

**Status:** ✅ Supabase client installed

### Step 2: Create Environment File

Copy and edit `.env`:
```bash
# Copy template
cp .env.example .env

# Edit with your keys (use notepad or any editor)
notepad .env
```

**Required values:**
```env
OPENAI_API_KEY=sk-proj-your-actual-openai-key-here
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_KEY=your-supabase-service-role-key
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
SECRET_KEY=any-random-secret-string-here
```

> **Note:** You can test without Supabase initially. Just leave those fields empty.

### Step 3: Start the Server

```bash
uvicorn app.main:app --reload --port 8004
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8004
INFO:     Application startup complete.
✓ Loaded 5 Q&A pairs
```

### Step 4: Test the Hybrid Endpoint

**Option A: Using the test script**
```bash
# Open a new terminal
python test_hybrid.py
```

**Option B: Using curl**
```bash
curl -X POST http://localhost:8004/api/v1/hybrid/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"test-user\",\"session_id\":\"sess-001\",\"prompt\":\"What is AI?\",\"mode\":\"balanced\"}"
```

**Option C: Using browser**
Open: http://localhost:8004/docs

Click on `POST /api/v1/hybrid/chat` → Try it out → Execute

### Step 5: Verify Response

You should see:
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

**Key indicators:**
- ✅ `source: "json_match"` = Answer came from knowledge base (free!)
- ✅ `tokens_used: 0` = No OpenAI API call (cost: $0)
- ✅ `processing_time: "0.01s"` = Super fast response

---

## 🧪 Testing Different Scenarios

### Test 1: JSON Match (Known Question)
```bash
curl -X POST http://localhost:8004/api/v1/hybrid/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user-1","session_id":"s1","prompt":"What is AI?","mode":"balanced"}'
```
**Expected:** `source: "json_match"`, `tokens_used: 0`

### Test 2: AI Fallback (Unknown Question)
```bash
curl -X POST http://localhost:8004/api/v1/hybrid/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user-1","session_id":"s1","prompt":"Explain quantum computing in simple terms","mode":"balanced"}'
```
**Expected:** `source: "ai_generated"`, `tokens_used: >0`

> **Note:** This requires a valid `OPENAI_API_KEY` in your `.env` file.

### Test 3: Creative Mode
```bash
curl -X POST http://localhost:8004/api/v1/hybrid/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user-1","session_id":"s1","prompt":"Write a haiku about AI","mode":"creative"}'
```
**Expected:** More creative, varied response (temp=0.9)

### Test 4: Precise Mode
```bash
curl -X POST http://localhost:8004/api/v1/hybrid/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user-1","session_id":"s1","prompt":"Define neural network","mode":"precise"}'
```
**Expected:** Concise, factual response (temp=0.3)

---

## 📊 Understanding the Response

```json
{
  "reply": "The actual answer text",
  "source": "json_match OR ai_generated",
  "session_id": "Your session ID echoed back",
  "tokens_used": 0,  // 0 for JSON, 50-300 for AI
  "processing_time": "0.01s",  // ~0.01s for JSON, ~1-3s for AI
  "timestamp": "2025-12-14T15:13:37Z"
}
```

**Source field tells you:**
- `json_match` = Answer from `data/knowledge_base.json` (free, fast)
- `ai_generated` = Answer from OpenAI API (costs tokens, slower)

---

## 🎯 Common Issues & Solutions

### Issue 1: "Module 'supabase' not found"
**Solution:**
```bash
pip install supabase
```

### Issue 2: "OPENAI_API_KEY not found"
**Solution:**
- Create `.env` file in project root
- Add: `OPENAI_API_KEY=sk-your-key-here`
- Restart server

### Issue 3: "Connection to Supabase failed"
**Solution:**
- This is OK for testing! The system will work without Supabase.
- History won't be saved, but chat will work.
- To fix: Add valid `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` to `.env`

### Issue 4: Port 8004 already in use
**Solution:**
```bash
# Use a different port
uvicorn app.main:app --reload --port 8005
```

### Issue 5: CORS errors from frontend
**Solution:**
Edit `app/main.py`, add your frontend URL to `origins` list:
```python
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Add your frontend URL
    "https://ai-chatbox.vercel.app"
]
```

---

## 📝 Next Steps

### 1. Expand Knowledge Base
Edit `data/knowledge_base.json`:
```json
[
  {"question": "What is AI?", "answer": "AI is..."},
  {"question": "What is machine learning?", "answer": "ML is..."},
  {"question": "What is deep learning?", "answer": "DL is..."},
  ... add more ...
]
```

**Tip:** Add 200-300 Q&A pairs for production use.

### 2. Get OpenAI API Key
1. Go to https://platform.openai.com
2. Sign up / Log in
3. Go to API Keys section
4. Create new secret key
5. Copy to `.env` file

### 3. Setup Supabase (Optional)
1. Go to https://supabase.com
2. Create new project
3. Go to Settings → API
4. Copy:
   - Project URL → `SUPABASE_URL`
   - Service Role Key → `SUPABASE_SERVICE_KEY`
5. Run SQL to create table (see README_HYBRID.md)

### 4. Deploy to Production
See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment guides.

---

## 🎓 Understanding the Hybrid System

```
Your Question: "What is AI?"
       ↓
┌──────────────────┐
│ 1. Normalize     │  "what is ai?"
└────────┬─────────┘
         ↓
┌──────────────────────────┐
│ 2. Search JSON KB        │
│    data/knowledge_base   │
└────────┬─────────────────┘
         ↓
    Found Match?
    ┌────┴────┐
   YES       NO
    │         │
    ↓         ↓
 Return    Call OpenAI
 (Free)    (Costs $)
    │         │
    └────┬────┘
         ↓
    Save to DB
         ↓
    Return Answer
```

**Benefits:**
- 💰 **Save money**: Common questions = $0
- ⚡ **Faster**: JSON lookup = 0.01s vs AI = 2s
- 🎯 **Consistent**: Same question = same answer
- 📊 **Trackable**: Know which answers are cached

---

## 🔗 Useful Links

- **API Docs (Interactive):** http://localhost:8004/docs
- **Health Check:** http://localhost:8004/api/v1/hybrid/
- **OpenAI Dashboard:** https://platform.openai.com/usage
- **Supabase Dashboard:** https://app.supabase.com

---

## ✅ Checklist

Before going to production:

- [ ] `.env` file created with all keys
- [ ] OpenAI API key added and tested
- [ ] Supabase project created and configured
- [ ] Knowledge base expanded (200+ Q&A pairs)
- [ ] Test suite passing (`python test_hybrid.py`)
- [ ] CORS origins updated for your frontend
- [ ] Server runs without errors
- [ ] Deployed to Render/Railway/Vercel

---

**Ready to go?** Run this command:

```bash
uvicorn app.main:app --reload --port 8004
```

Then visit: http://localhost:8004/docs

**Happy coding! 🚀**
